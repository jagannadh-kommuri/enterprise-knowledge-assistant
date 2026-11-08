import pytest
from fastapi.testclient import TestClient
from app.main import Provider, create_app

ADMIN = 'administrator-test-password'
READER = 'reader-test-password-long'

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('ADMIN_PASSWORD', ADMIN)
    monkeypatch.setenv('READER_PASSWORD', READER)
    monkeypatch.setenv('COOKIE_SECURE', 'false')
    monkeypatch.setenv('AI_MODE', 'preview')
    monkeypatch.setenv('DATABASE_PATH', str(tmp_path/'db.sqlite3'))
    with TestClient(create_app()) as c:
        yield c

def login(c, password=ADMIN):
    assert c.post('/api/login', json={'password':password}).status_code == 200

def add(c, title='Incident handbook', visibility='team', content='A severity one incident requires the on-call engineer to acknowledge the alert within five minutes. Publish incident updates every fifteen minutes.'):
    return c.post('/api/documents', json={'title':title,'content':content,'visibility':visibility})

def test_no_anonymous_access(client):
    assert client.get('/health').json()=={'status':'ok'}
    for route in ('/api/me','/api/documents','/api/metrics'):
        assert client.get(route).status_code==401
    assert client.post('/api/ask',json={'question':'incident?'}).status_code==401
    assert client.post('/api/login',json={'password':'wrong'}).status_code==401

def test_full_flow_citations_metrics_and_delete(client):
    login(client)
    doc=add(client)
    assert doc.status_code==201
    result=client.post('/api/ask',json={'question':'When do we acknowledge an incident alert?'}).json()
    assert result['sources'][0]['title']=='Incident handbook'
    assert '[1]' in result['answer'] and 'five minutes' in result['answer']
    assert result['mode']=='preview' and result['tokens']==0
    assert client.get('/api/metrics').json()['requests']==1
    assert client.delete('/api/documents/'+doc.json()['id']).status_code==200
    assert client.get('/api/documents').json()==[]
    assert client.delete('/api/documents/missing').status_code==404

def test_reader_cannot_retrieve_or_modify_admin_documents(client):
    login(client)
    add(client, title='Restricted launch', visibility='admin', content='The secret codename for the upcoming launch is violetmonsoon. Launch approval requires the executive team.')
    login(client,READER)
    assert client.get('/api/documents').json()==[]
    result=client.post('/api/ask',json={'question':'What is the violetmonsoon launch codename?'}).json()
    assert result['sources']==[]
    assert 'violetmonsoon' not in result['answer']
    assert add(client).status_code==403
    assert client.delete('/api/documents/anything').status_code==403
    assert client.get('/api/metrics').status_code==403

def test_reader_can_retrieve_team_document(client):
    login(client);add(client);login(client,READER)
    assert len(client.get('/api/documents').json())==1
    assert client.post('/api/ask',json={'question':'incident alert'}).json()['sources']

def test_no_evidence_and_bad_input(client):
    login(client);add(client)
    result=client.post('/api/ask',json={'question':'astrophysics quasars'}).json()
    assert result['sources']==[]
    assert 'could not find enough evidence' in result['answer']
    assert client.post('/api/ask',json={'question':'the and for'}).status_code==422
    assert client.post('/api/documents',json={'title':' ','content':' '*10}).status_code==422
    assert client.post('/api/ask',json={'question':'x'*1501}).status_code==422

def test_cross_origin_and_logout(client):
    assert client.post('/api/login',headers={'origin':'https://attacker.invalid'},json={'password':ADMIN}).status_code==403
    login(client)
    login_response = client.post('/api/login', json={'password': ADMIN})
    cookie = login_response.headers['set-cookie'].lower()
    assert 'httponly' in cookie and 'samesite=strict' in cookie and 'max-age=3600' in cookie
    assert client.get('/').headers['content-security-policy'].startswith("default-src 'self'")
    client.post('/api/logout')
    assert client.get('/api/me').status_code==401

def test_login_rate_limit(client):
    for _ in range(10):
        assert client.post('/api/login',json={'password':'bad'}).status_code==401
    assert client.post('/api/login',json={'password':'bad'}).status_code==429

def test_fail_closed_config(monkeypatch):
    monkeypatch.setenv('ADMIN_PASSWORD','short')
    with pytest.raises(RuntimeError):create_app()
    monkeypatch.setenv('AI_MODE','azure')
    monkeypatch.delenv('AZURE_OPENAI_API_KEY',raising=False)
    with pytest.raises(RuntimeError):Provider()

def test_provider_contract_and_citation_validation(monkeypatch):
    monkeypatch.setenv('AI_MODE','azure')
    for k,v in {'AZURE_OPENAI_ENDPOINT':'https://example.openai.azure.com','AZURE_OPENAI_API_KEY':'test','AZURE_OPENAI_CHAT_DEPLOYMENT':'chat','AZURE_OPENAI_EMBEDDING_DEPLOYMENT':'embed'}.items():monkeypatch.setenv(k,v)
    p=Provider()
    def fake(route,body):
        if route=='embeddings':
            assert body['model']=='embed'
            return {'data':[{'index':0,'embedding':[1.0,0.0]}],'usage':{'total_tokens':3}}
        assert body['model']=='chat'
        assert body['messages'][0]['role']=='system'
        return {'choices':[{'message':{'content':'A supported answer [1]'}}],'usage':{'total_tokens':20}}
    monkeypatch.setattr(p,'call',fake)
    assert p.embed(['incident'])[1]==3
    assert p.answer('incident',[{'title':'Handbook','text':'A fact'}])==('A supported answer [1]',20)
    monkeypatch.setattr(p,'call',lambda *a: {'choices':[{'message':{'content':'Made up [99]'}}]})
    with pytest.raises(Exception) as e:p.answer('x',[{'title':'x','text':'y'}])
    assert e.value.status_code==502

def test_provider_failure_is_recorded_without_secret(client,monkeypatch):
    login(client)
    def fail(*args):
        from fastapi import HTTPException
        raise HTTPException(502,'AI provider unavailable')
    monkeypatch.setattr(client.app.state.provider,'embed',fail)
    assert client.post('/api/ask',json={'question':'incident alert'}).status_code==502
    assert client.get('/api/metrics').json()['failures']==1

def test_index_model_change_requires_reindex(client,monkeypatch):
    monkeypatch.setenv('AI_MODE','azure')
    for k,v in {'AZURE_OPENAI_ENDPOINT':'https://example.openai.azure.com','AZURE_OPENAI_API_KEY':'test','AZURE_OPENAI_CHAT_DEPLOYMENT':'chat','AZURE_OPENAI_EMBEDDING_DEPLOYMENT':'embed'}.items():monkeypatch.setenv(k,v)
    with pytest.raises(RuntimeError,match='Embedding configuration changed'):create_app()

def test_session_survives_new_application_instance(client):
    login(client)
    cookie = client.cookies.get('atlas_session')
    with TestClient(create_app()) as second:
        second.cookies.set('atlas_session', cookie)
        assert second.get('/api/me').status_code == 200
        second.post('/api/logout')
    assert client.get('/api/me').status_code == 401


def test_password_change_revokes_existing_session(client, monkeypatch):
    login(client)
    monkeypatch.setenv('ADMIN_PASSWORD', 'rotated-admin-password-long')
    with TestClient(create_app()) as second:
        second.cookies.set('atlas_session', client.cookies.get('atlas_session'))
        assert second.get('/api/me').status_code == 401


def test_rate_limits_shared_across_application_instances(client):
    for _ in range(10):
        assert client.post('/api/login', json={'password': 'bad'}).status_code == 401
    with TestClient(create_app()) as second:
        assert second.post('/api/login', json={'password': ADMIN}).status_code == 429


def test_database_stores_only_hashed_session_token(client):
    login(client)
    with client.app.state.db() as con:
        row = con.execute('SELECT token_hash FROM sessions').fetchone()
        assert len(row['token_hash']) == 64
        assert row['token_hash'] != client.cookies.get('atlas_session')
        con.execute('UPDATE sessions SET expires=0')
    assert client.get('/api/me').status_code == 401


def test_vercel_rejects_ephemeral_storage(monkeypatch):
    from app.storage import database
    monkeypatch.setenv('VERCEL', '1')
    monkeypatch.delenv('DATABASE_URL', raising=False)
    with pytest.raises(RuntimeError, match='PostgreSQL'): database()
    monkeypatch.setenv('DATABASE_URL', 'sqlite://temporary')
    with pytest.raises(RuntimeError, match='PostgreSQL'): database()


def test_production_interface_has_no_preview_role_controls_enabled(client):
    html=client.get('/').text
    assert 'Research desk' in html and 'Add a document' in html
    assert client.get('/static/config.js').text.strip() == 'export const REVIEW = false;'
    assert client.get('/static/samples.json').status_code == 200

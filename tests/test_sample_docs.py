from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.mark.parametrize('filename,question,expected',[
 ('incident-response.md','When is an incident postmortem due?','three business days'),
 ('access-policy.md','When does production access expire?','thirty days'),
 ('onboarding.md','What should a new engineer do during the first week?','documentation pull request'),
 ('restricted-launch.md','What is the violetmonsoon launch review date?','December 10, 2026'),
])
def test_shipped_document_retrieval(tmp_path,monkeypatch,filename,question,expected):
    monkeypatch.setenv('ADMIN_PASSWORD','sample-docs-test-password')
    monkeypatch.setenv('AI_MODE','preview')
    monkeypatch.setenv('COOKIE_SECURE','false')
    monkeypatch.setenv('DATABASE_PATH',str(tmp_path/'samples.sqlite3'))
    with TestClient(create_app()) as client:
        assert client.post('/api/login',json={'password':'sample-docs-test-password'}).status_code==200
        content=(Path(__file__).parents[1]/'sample_docs'/filename).read_text()
        assert client.post('/api/documents',json={'title':filename,'content':content,'visibility':'admin' if filename.startswith('restricted') else 'team'}).status_code==201
        result=client.post('/api/ask',json={'question':question})
        assert result.status_code==200
        data=result.json()
        assert data['sources'] and data['sources'][0]['title']==filename
        assert expected.lower() in data['answer'].lower()

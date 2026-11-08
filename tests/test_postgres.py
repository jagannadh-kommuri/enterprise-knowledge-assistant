"""Optional real PostgreSQL test, isolated in a throwaway schema."""
import os
import secrets
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
import pytest
from fastapi.testclient import TestClient
from app.main import create_app


def test_postgres_ingestion_sessions_and_authorization(monkeypatch):
    url = os.getenv('TEST_DATABASE_URL')
    if not url:
        pytest.skip('TEST_DATABASE_URL not configured; real PostgreSQL integration unverified')
    import psycopg
    schema = 'atlas_test_' + secrets.token_hex(8)
    with psycopg.connect(url, autocommit=True) as connection:
        connection.execute('CREATE SCHEMA ' + schema)
    parsed=urlsplit(url)
    query=dict(parse_qsl(parsed.query))
    query['options']='-c search_path='+schema
    isolated=urlunsplit(parsed._replace(query=urlencode(query)))
    monkeypatch.setenv('DATABASE_URL',isolated)
    monkeypatch.setenv('ADMIN_PASSWORD','postgres-admin-test-password')
    monkeypatch.setenv('READER_PASSWORD','postgres-reader-test-password')
    monkeypatch.setenv('AI_MODE','preview')
    monkeypatch.setenv('COOKIE_SECURE','false')
    monkeypatch.setenv('INIT_SCHEMA','true')
    try:
        with TestClient(create_app()) as client:
            assert client.post('/api/login',json={'password':'postgres-admin-test-password'}).status_code==200
            response=client.post('/api/documents',json={'title':'PG integration handbook','content':'The fictional auroraplan release requires manager approval before deployment.','visibility':'admin'})
            assert response.status_code==201
            assert client.post('/api/ask',json={'question':'auroraplan release'}).json()['sources']
            cookie=client.cookies.get('atlas_session')
            monkeypatch.setenv('VERCEL','1')
            monkeypatch.setenv('INIT_SCHEMA','false')
            with TestClient(create_app()) as second:
                second.cookies.set('atlas_session',cookie)
                assert len(second.get('/api/documents').json())==1
                assert second.get('/api/metrics').status_code==200
                assert second.post('/api/login',json={'password':'postgres-reader-test-password'}).status_code==200
                assert second.get('/api/documents').json()==[]
    finally:
        with psycopg.connect(url,autocommit=True) as connection:
            connection.execute('DROP SCHEMA '+schema+' CASCADE')

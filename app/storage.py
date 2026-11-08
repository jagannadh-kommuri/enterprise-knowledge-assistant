"""Small SQL bridge: SQLite for local review, PostgreSQL for serverless hosting."""
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

class Connection:
    def __init__(self, connection, postgres):
        self.connection, self.postgres = connection, postgres

    def execute(self, query, params=()):
        if self.postgres:
            query = query.replace('?', '%s')
        return self.connection.execute(query, params)

    def executemany(self, query, rows):
        if self.postgres:
            with self.connection.cursor() as cursor:
                cursor.executemany(query.replace('?', '%s'), rows)
        else:
            self.connection.executemany(query, rows)

    def executescript(self, script):
        for statement in script.split(';'):
            if statement.strip():
                self.execute(statement)


def database():
    url = os.getenv('DATABASE_URL', '')
    if os.getenv('VERCEL') and not url:
        raise RuntimeError('Vercel requires a persistent PostgreSQL DATABASE_URL')
    postgres = bool(url)
    if postgres and not url.startswith(('postgres://', 'postgresql://')):
        raise RuntimeError('DATABASE_URL must be a PostgreSQL connection URL')
    path = Path(os.getenv('DATABASE_PATH', './data/atlas.sqlite3'))
    if not postgres:
        path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connect():
        if postgres:
            import psycopg
            from psycopg.rows import dict_row
            con = psycopg.connect(url, row_factory=dict_row, connect_timeout=10)
        else:
            con = sqlite3.connect(path, timeout=20)
            con.row_factory = sqlite3.Row
            con.execute('PRAGMA foreign_keys=ON')
        try:
            with con:
                yield Connection(con, postgres)
        finally:
            con.close()
    return connect

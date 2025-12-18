import pytest
import psycopg2
from psycopg2.extras import RealDictCursor


@pytest.fixture(scope="session")
def pg_connection():
    """Establish a connection to PostgresSQL database."""
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="testdb",
        user="test",
        password="test"
    )
    yield conn
    conn.close()


@pytest.fixture
def pg_cursor(pg_connection):
    """Get a cursor for each test"""
    cursor = pg_connection.cursor(cursor_factory=RealDictCursor)
    yield cursor
    pg_connection.rollback()
    cursor.close()

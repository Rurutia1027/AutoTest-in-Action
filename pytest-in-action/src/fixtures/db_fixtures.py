import pytest
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


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


@pytest.fixture(scope="session")
def pg_cursor(pg_connection):
    """Get a cursor for each test"""
    cursor = pg_connection.cursor(cursor_factory=RealDictCursor)
    yield cursor
    pg_connection.rollback()
    cursor.close()


# Utility: generate unique names per test
def unique_name(base_name):
    return f"{base_name}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"


# Cleanup functions
def cleanup_table(cursor, table_name):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
    cursor.connection.commit()


def cleanup_schema(cursor, schema_name):
    cursor.execute(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE;")
    cursor.connection.commit()


def cleanup_database(cursor, db_name):
    # Only feasible for dedicated test DB, otherwise reset all schemas
    cursor.execute("""
                   SELECT schema_name
                   FROM information_schema.schemata
                   WHERE schema_name NOT IN ('information_schema', 'pg_catalog')
                   """)
    schemas = cursor.fetchall()
    for schema in schemas:
        cleanup_schema(cursor, schema['schema_name'])

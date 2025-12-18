# src/tests/functional/test_postgres_basic.py

from src.fixtures.db_fixtures import pg_cursor, pg_connection


def test_create_table(pg_connection, pg_cursor):
    pg_cursor.execute("CREATE TABLE IF NOT EXISTS test_table(id SERIAL PRIMARY KEY, name TEXT);")
    pg_cursor.execute("SELECT * FROM test_table;")
    pg_connection.commit()
    result = pg_cursor.fetchall()
    assert result == []


def test_insert_data(pg_connection, pg_cursor):
    pg_cursor.execute("INSERT INTO test_table(name) VALUES(%s)", ("Alice",))
    pg_cursor.execute("SELECT name FROM test_table WHERE name=%s", ("Alice",))
    result = pg_cursor.fetchone()
    assert result["name"] == "Alice"

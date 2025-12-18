# src/tests/functional/test_postgres_basic.py

import pytest
from src.fixtures.db_fixtures import pg_cursor, unique_name, cleanup_table, cleanup_schema

@pytest.mark.functional
@pytest.mark.postgres
def test_create_table(pg_cursor):
    table_name = unique_name("test_table")
    pg_cursor.execute(f"CREATE TABLE {table_name}(id SERIAL PRIMARY KEY, name TEXT);")
    pg_cursor.execute(f"SELECT * FROM {table_name};")
    result = pg_cursor.fetchall()
    assert result == []
    cleanup_table(pg_cursor, table_name)

@pytest.mark.functional
@pytest.mark.postgres
def test_insert_data(pg_cursor):
    table_name = unique_name("test_table")
    pg_cursor.execute(f"CREATE TABLE {table_name}(id SERIAL PRIMARY KEY, name TEXT);")
    pg_cursor.execute(f"INSERT INTO {table_name}(name) VALUES('Alice');")
    pg_cursor.execute(f"SELECT name FROM {table_name} WHERE name='Alice';")
    result = pg_cursor.fetchone()
    assert result["name"] == "Alice"
    cleanup_table(pg_cursor, table_name)

@pytest.mark.functional
@pytest.mark.postgres
def test_create_multiple_databases(pg_cursor):
    # Note: PostgreSQL does not allow creating DB from the same connection, normally need a superuser or separate connection
    # For isolation, we just create schemas instead
    schemas = [unique_name(f"schema{i}") for i in range(1, 4)]
    for schema in schemas:
        pg_cursor.execute(f"CREATE SCHEMA {schema};")
    pg_cursor.connection.commit()
    # Verify creation
    for schema in schemas:
        pg_cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name='{schema}';")
        assert pg_cursor.fetchone()["schema_name"] == schema
    # Cleanup
    for schema in schemas:
        cleanup_schema(pg_cursor, schema)

@pytest.mark.functional
@pytest.mark.postgres
def test_create_tables_in_schemas(pg_cursor):
    schemas = [unique_name(f"schema{i}") for i in range(1, 4)]
    tables = ["users", "products", "shops"]
    for schema in schemas:
        pg_cursor.execute(f"CREATE SCHEMA {schema};")
    pg_cursor.execute(f"CREATE TABLE {schemas[0]}.{tables[0]}(id SERIAL PRIMARY KEY, name TEXT);")
    pg_cursor.execute(f"CREATE TABLE {schemas[1]}.{tables[1]}(id SERIAL PRIMARY KEY, name TEXT);")
    pg_cursor.execute(f"CREATE TABLE {schemas[2]}.{tables[2]}(id SERIAL PRIMARY KEY, name TEXT, address TEXT);")
    pg_cursor.connection.commit()
    # Cleanup
    for schema in schemas:
        cleanup_schema(pg_cursor, schema)

@pytest.mark.functional
@pytest.mark.postgres
def test_insert_data_in_multiple_schemas(pg_cursor):
    schemas = [unique_name(f"schema{i}") for i in range(1, 4)]
    tables = ["users", "products", "shops"]
    for schema in schemas:
        pg_cursor.execute(f"CREATE SCHEMA {schema};")
    pg_cursor.execute(f"CREATE TABLE {schemas[0]}.{tables[0]}(id SERIAL PRIMARY KEY, name TEXT);")
    pg_cursor.execute(f"CREATE TABLE {schemas[1]}.{tables[1]}(id SERIAL PRIMARY KEY, name TEXT);")
    pg_cursor.execute(f"CREATE TABLE {schemas[2]}.{tables[2]}(id SERIAL PRIMARY KEY, name TEXT, address TEXT);")
    # Insert data
    pg_cursor.execute(f"INSERT INTO {schemas[0]}.{tables[0]}(name) VALUES('Alice');")
    pg_cursor.execute(f"INSERT INTO {schemas[1]}.{tables[1]}(name) VALUES('Widget');")
    pg_cursor.execute(f"INSERT INTO {schemas[2]}.{tables[2]}(name, address) VALUES('SuperMart','123 Main St');")
    pg_cursor.connection.commit()
    # Validate
    pg_cursor.execute(f"SELECT name FROM {schemas[0]}.{tables[0]};")
    assert pg_cursor.fetchone()["name"] == "Alice"
    pg_cursor.execute(f"SELECT name FROM {schemas[1]}.{tables[1]};")
    assert pg_cursor.fetchone()["name"] == "Widget"
    pg_cursor.execute(f"SELECT name, address FROM {schemas[2]}.{tables[2]};")
    result = pg_cursor.fetchone()
    assert result["name"] == "SuperMart"
    assert result["address"] == "123 Main St"
    # Cleanup
    for schema in schemas:
        cleanup_schema(pg_cursor, schema)

@pytest.mark.functional
@pytest.mark.postgres
def test_query_inserted_data(pg_cursor):
    table_name = unique_name("query_table")
    pg_cursor.execute(f"CREATE TABLE {table_name}(id SERIAL PRIMARY KEY, name TEXT);")
    pg_cursor.execute(f"INSERT INTO {table_name}(name) VALUES('Bob');")
    pg_cursor.execute(f"SELECT * FROM {table_name} WHERE name='Bob';")
    result = pg_cursor.fetchone()
    assert result["name"] == "Bob"
    cleanup_table(pg_cursor, table_name)

@pytest.mark.functional
@pytest.mark.postgres
def test_delete_data(pg_cursor):
    table_name = unique_name("delete_table")
    pg_cursor.execute(f"CREATE TABLE {table_name}(id SERIAL PRIMARY KEY, name TEXT);")
    pg_cursor.execute(f"INSERT INTO {table_name}(name) VALUES('Charlie');")
    pg_cursor.execute(f"DELETE FROM {table_name} WHERE name='Charlie';")
    pg_cursor.execute(f"SELECT * FROM {table_name} WHERE name='Charlie';")
    result = pg_cursor.fetchall()
    assert result == []
    cleanup_table(pg_cursor, table_name)

@pytest.mark.functional
@pytest.mark.postgres
def test_update_data(pg_cursor):
    table_name = unique_name("update_table")
    pg_cursor.execute(f"CREATE TABLE {table_name}(id SERIAL PRIMARY KEY, name TEXT);")
    pg_cursor.execute(f"INSERT INTO {table_name}(name) VALUES('David');")
    pg_cursor.execute(f"UPDATE {table_name} SET name='Dave' WHERE name='David';")
    pg_cursor.execute(f"SELECT name FROM {table_name} WHERE id=1;")
    assert pg_cursor.fetchone()["name"] == "Dave"
    cleanup_table(pg_cursor, table_name)

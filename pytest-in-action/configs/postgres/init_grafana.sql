-- create database and user
CREATE DATABASE grafana;
CREATE USER grafana WITH PASSWORD 'grafana';

-- grant privileges on the database
GRANT ALL PRIVILEGES ON DATABASE grafana TO grafana;

-- grant privileges on public schema
\c grafana
ALTER SCHEMA public OWNER TO grafana;
GRANT ALL PRIVILEGES ON SCHEMA public TO grafana;

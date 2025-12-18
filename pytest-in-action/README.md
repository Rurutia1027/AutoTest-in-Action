# PyTest-in-Actoin: MySQL + Prometheus + BDD 
## High-Level Architecture 
**Components:**
- MySQL - Main database service for functional testing. 
- Prometheus - Monitoring service to collect metrics from MySQL.
- MySQL Exporter - Provides metrics via REST API for Prometheus 
- PyTest - Primary automation framework 
- BDD Layer (Behave / PyTest-BDD) - 

**Flow**
- Docker Compose starts MySQL, Exporter, and Prometheus
- PyTest fixtures initialize connections and environment.
- Test scenarios (functional, integration, regression) run against:
> MySQL direct (via SQL queries)
> Prometheus metrics (via REST API)
- BDD-style scenarios organize and orchestrate the test cases. 
- Reports are generated for all executions. 


## Requirements (Python Packages)
```text
# PyTest core 
pytest==8.0.0
pytest-html==3.2.0
pytest-bdd==4.1.0

# Database
mysql-connector-python==8.1.0

# REST API requests
requests==2.32.0

# Optional: for visual regression snapshots
Pillow==10.0.0
playwright==1.46.0
```

**Installation command**
```bash
pip install -r requirements.txt
playwright install 
```


## Docker Compose for Test Environment
```yaml 
services:
  mysql: 
    image: mysql:8.0
    container_name: test-mysql
    environment:
      MYSQL_ROOT_PASSWORD: admin
      MYSQL_DATABASE: mysql
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      retries: 5
  mysqld-exporter:
    image: prom/mysqld-exporter
    container_name: mysqld-exporter
    environment:
      DATA_SOURCE_NAME: "root:root@(mysql:3306)"
    ports:
      - "9104:9104"
    depends_on:
      mysql:
        condition: service_healthy
  prometheus:
    image: prom/prometheus
    container_name:
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    depends_on:
      - mysqld-exporter
```

**prometheus.yml** (basic config to scrape MySQL exporter metrics):
```yaml 
global:
  scrape_intervals: 15s
scrape_configs:
  - job_name: 'mysql'
    static_configs:
      - targets: ['mysqld-exporter:9104']
```


## PyTest Tutorial Structure 

```
pytest-in-action/
│
├── README.md
├── docker-compose.yml
├── prometheus.yml
├── requirements.txt
│
├── fixtures/                        # PyTest fixtures for environment setup
│   ├── db_fixtures.py               # MySQL-related fixtures
│   └── prometheus_fixtures.py       # Prometheus-related fixtures
│
├── tests/
│   ├── functional/                  # Functional tests (MySQL, basic queries)
│   │   ├── test_mysql_basic.py
│   │   ├── test_mysql_insert.py
│   │   ├── test_mysql_queries.py
│   │   └── test_mysql_data.py
│   │
│   ├── integration/                 # Integration tests (MySQL + Prometheus)
│   │   ├── test_mysql_metrics.py
│   │   └── test_prometheus_metrics.py
│   │
│   ├── regression/                  # Regression tests for both MySQL & Prometheus
│   │   └── test_regression_suite.py
│   │
│   └── vdd/                         # BDD-style / Visual Driven scenarios
│       ├── features/
│       │   ├── mysql.feature
│       │   └── prometheus.feature
│       │
│       └── steps/
│           ├── test_mysql_steps.py
│           └── test_prometheus_steps.py
│
└── reports/
    └── html/                        # Test reports, VDD snapshots, and screenshots

```

## Key PyTest Concepts Used 
### Fixtures 
- Setup MySQL connections
- Setup Prometheus REST API client
- Isolate test environment 

### BDD Integration 
- Use **pytest-bdd** plugin
- Map `.feature` steps to Python step functions 
- Organize tests by **scenarios and topics**

### Assertions 
- Functional: verify query results
- Integration: verify Prometheus metrics

### Parametrization 
- Test multiple query variations
- Test multiple metric thresholds

### Regression 
- Capture baseline state 
- Compare new results to previous runs 

### Reporting 
- HTML or JSON report 
- Include scenario descriptio, result, and context


## Example Functional Test (MySQL)
```python 
import pytest
import mysql.connector 

@pytest.fixture(scope="session")
def db_conn():
    conn = mysql.connector.connect(
        host="localhost", user="root", password="root", database="test_db"
    )
    yield conn 
    conn.close()

def test_insert_and_query(db_conn):
    cursor = db_conn.cursor()
    custor.execute("CREATE TABLE IF NOT EXISTS test (id INT PRIMARYKEY, name VARCHAR(20)); ")
    cursor.execute("INSERT INTO test(id, name) VALUES (1, 'Alice');")
    db_conn.commit()
    
    cursor.execute("SELECT name FROM test WHERE id = 1;")
    result = cursor.fetchone()
    assert result[0] == "Alice"
```

## Example BDD Feature (mysql.feature)

**BDD Gherkin**

```gherkin
Feature: MySQL data validation 
  Scenario: Insert a new record and verify 
    Given a MySQL connection is establish
    When I insert a record with id 1 and name "Alice"
    Then the record with id 1 should exist and nameshould be "Alice"
```

**Step Defintion (`test_mysql_steps.py`)**
```python 
from pytest_bdd import scenarios, given, when, then 
import mysql.connector
import pytest

scenarios('../features/mysql.feature')

@pytest.fixture # like spring context, global variables & contexts holder 
def db_conn():
    conn = mysql.connector.connect(
        host="localhost", user="root", password="root", database="test_db"
    )
    yield conn
    conn.close()

@given("a MySQL connection is established")    
def connection(db_conn):
    return db_conn

@when('I insert a record with id 1 and name "Alice"')
def insert_record(connection):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO test (id,  name) VALUES (1, 'Alice'); ")
    connection.commit()

@then('the record with id 1 should exist and name should be "Alice"')
def verify_record(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM test WHERE id=1;")
    result = cursor.fetchone()
    assert result[0] == "Alice"
```

## Integrate with Prometheus Metrics 
- Use **Python request** to query Prometheus REST API:
```python 
import requests

def test_mysql_metric(); 
  response = requests.get('http://localhost:9000/api/v1/query', params=('query':'mysql_global_status_connections'))
  data = response.json()
  assert 'data' in data 
```


## Running Tests 

```bash 
# Start Docker environment
docker compose up -d 

# Run all PyTest tests 
pytest -v --html=reports/html/test_report.html 
```




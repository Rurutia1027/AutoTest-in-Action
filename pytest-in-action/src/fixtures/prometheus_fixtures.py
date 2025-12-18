import os
import requests
import pytest
from dotenv import load_dotenv

# load env variables
load_dotenv()

PROMETHEUS_URL = os.environ.get("PROMETHEUS_URL")


@pytest.fixture(scope="session")
def prometheus_url():
    return PROMETHEUS_URL


@pytest.fixture(scope="session")
def query_prometheus():
    def _query(query: str):
        r = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": query})
        r.raise_for_status()
        return r.json()

    return _query


@pytest.fixture(scope="session")
def query_range_prometheus():
    def _query_range(query: str, start: str, end: str, step: str = "30s"):
        r = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query_range",
            params={"query": query, "start": start, "end": end, "step": step},
        )
        r.raise_for_status()
        return r.json()

    return _query_range

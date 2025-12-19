# src/tests/functional/test_prometheus_api.py

import pytest
import requests

from src.fixtures.prometheus_fixtures import query_prometheus, query_range_prometheus, prometheus_url


# ---------- /api/v1/query_range ----------

@pytest.mark.functional
@pytest.mark.prometheus
def test_query_pg_up(query_prometheus):
    # check postgres exporter metric exists
    result = query_prometheus("pg_up")
    assert "data" in result
    assert len(result["data"]["result"]) > 0


@pytest.mark.functional
@pytest.mark.prometheus
def test_query_range_empty_metric(query_range_prometheus):
    import time
    end = int(time.time())
    start = end - 60
    result = query_range_prometheus("non_existing_metric", str(start), str(end))
    assert "data" in result
    assert result["data"]["result"] == []

# ---------- /api/v1/targets ----------
@pytest.mark.functional
@pytest.mark.prometheus
def test_targets_up(prometheus_url):
    r = requests.get(f"{prometheus_url}/api/v1/targets")
    r.raise_for_status()
    data = r.json()
    assert any(t["health"] == "up" for t in data["data"]["activeTargets"])


@pytest.mark.functional
@pytest.mark.prometheus
def test_targets_format(prometheus_url):
    r = requests.get(f"{prometheus_url}/api/v1/targets")
    r.raise_for_status()
    data = r.json()
    assert "data" in data
    assert "activeTargets" in data["data"]
    assert data["data"]["droppedTargets"] == []

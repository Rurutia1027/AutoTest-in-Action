import requests
import pytest
import time

from src.fixtures.prometheus_fixtures import prometheus_url


@pytest.mark.functional
@pytest.mark.prometheus
def test_series_with_up_metric(prometheus_url):
    """Validate basic series listing using built-in 'up' metric"""
    resp = requests.get(f"{prometheus_url}/api/v1/series", params={"match[]": "up"})

    assert resp.status_code == 200
    payload = resp.json()

    assert payload["status"] == "success"
    assert isinstance(payload["data"], list)
    assert len(payload["data"]) > 0


@pytest.mark.functional
@pytest.mark.prometheus
def test_series_with_job_selector(prometheus_url):
    """Validate series filtering by job label"""
    resp = requests.get(
        f"{prometheus_url}/api/v1/series",
        params={"match[]": '{job="postgres"}'}
    )
    payload = resp.json()
    assert payload["status"] == "success"
    for series in payload["data"]:
        assert series["job"] == "postgres"

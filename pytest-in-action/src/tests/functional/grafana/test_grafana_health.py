# tests/functional/grafana/health/test_grafana_health.py

import pytest
from src.fixtures.grafana_fixtures import grafana_context, grafana_request

@pytest.mark.functional
@pytest.mark.grafana
def test_grafana_health_status(grafana_request):
    """
    Test Grafana core health API.
    """
    resp = grafana_request("GET", "/api/health")
    assert resp["database"] == "ok"
    assert "version" in resp
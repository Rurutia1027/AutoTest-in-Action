import pytest
from src.fixtures.grafana_fixtures import grafana_request, unique_dashboard, grafana_context


@pytest.mark.functional
@pytest.mark.grafana
def test_create_dashboard(grafana_request, unique_dashboard):
    payload = unique_dashboard
    resp = grafana_request("POST", "/api/dashboards/db", json=payload)
    assert resp["status"] == "success"
    assert "id" in resp
    assert resp["slug"] == payload["dashboard"]["title"].lower()


@pytest.mark.functional
@pytest.mark.grafana
def test_get_dashboard(grafana_request, unique_dashboard):
    payload = unique_dashboard
    create_resp = grafana_request("POST", "/api/dashboards/db", json=payload)
    uid = create_resp["uid"]

    get_resp = grafana_request("GET", f"/api/dashboards/uid/{uid}")
    assert get_resp['meta']["slug"] == payload["dashboard"]["title"].lower()


@pytest.mark.functional
@pytest.mark.grafana
def test_delete_dashboard(grafana_request, unique_dashboard):
    payload = unique_dashboard
    create_resp = grafana_request("POST", "/api/dashboards/db", json=payload)
    uid = create_resp["uid"]

    grafana_request("DELETE", f"/api/dashboards/uid/{uid}")

    # verify deletion
    with pytest.raises(Exception):
        grafana_request("GET", f"/api/dashboards/uid/{uid}")
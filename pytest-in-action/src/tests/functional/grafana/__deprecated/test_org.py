# # tests/functional/grafana/health/test_health.py
#
# import pytest
# import requests
#
# from src.fixtures.prometheus_fixtures import random_suffix
# from src.fixtures.grafana_fixtures import grafana_request, grafana_context
#
#
# @pytest.mark.functional
# @pytest.mark.grafana
# def test_create_org(grafana_request):
#     """Create a new organization."""
#     org_name = f"pytest-org-create-{random_suffix()}"
#     resp = grafana_request("POST", "api/orgs", json={"name": org_name})
#     assert "orgId" in resp
#     assert resp["orgId"] > 0
#
#
# @pytest.mark.functional
# @pytest.mark.grafana
# def test_get_org(grafana_request):
#     """Get an organization."""
#     # First, create org
#     org_name = f"pytest-org-get-{random_suffix()}"
#     create_resp = grafana_request("POST", "api/orgs", json={"name": org_name})
#     org_id = create_resp["orgId"]
#
#     # Then, get org
#     resp = grafana_request("GET", f"api/orgs/{org_id}")
#     assert resp["name"] == org_name
#     assert resp["id"] == org_id
#
#
# @pytest.mark.functional
# @pytest.mark.grafana
# def test_update_org(grafana_request):
#     """Update an organization."""
#     org_name = f"pytest-org-update-{random_suffix()}"
#     create_resp = grafana_request("POST", "api/orgs", json={"name": org_name})
#     org_id = create_resp["orgId"]
#
#     new_name = f"pytest-org-update-new-{random_suffix()}"
#     resp = grafana_request("PUT", f"api/orgs/{org_id}", json={"name": new_name})
#     assert resp["message"] == "Organization updated"
#
#     # Verify update
#     org = grafana_request("GET", f"api/orgs/{org_id}")
#     assert org["name"] == new_name
#
#
# @pytest.mark.functional
# @pytest.mark.grafana
# def test_delete_org(grafana_request):
#     """Delete an organization"""
#     org_name = f"pytest-org-delete-{random_suffix()}"
#     create_resp = grafana_request("POST", "api/orgs", json={"name": org_name})
#     org_id = create_resp["orgId"]
#
#     resp = grafana_request("DELETE", f"api/orgs/{org_id}")
#     # Grafana may return 200 OK with empty body
#     assert resp["message"] == "Organization deleted"
#
#     # Verify deletion fails
#     with pytest.raises(requests.HTTPError):
#         grafana_request("GET", f"api/orgs/{org_id}")

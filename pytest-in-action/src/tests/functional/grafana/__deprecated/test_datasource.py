# import pytest
# import uuid
# from src.fixtures.grafana_fixtures import grafana_request, grafana_context, unique_datasource
#
# @pytest.mark.functional
# @pytest.mark.grafana
# def test_grafana_create_and_get_update_delete_datasource(grafana_request, unique_datasource):
#     """
#     Full CRUD test for Grafana dashboard using Prometheus as datasource instances
#     """
#     # --- CREATE ---
#     ds_name = f"MyPrometheus-{uuid.uuid4().hex[:6]}"
#     datasource_payload = {
#         "name": ds_name,
#         "type": "prometheus",
#         "access": "proxy",
#         "url": "http://prometheus:9090",
#         "isDefault": False,
#         "jsonData": {}
#     }
#
#     create_resp = grafana_request("POST", "/api/datasources", json=datasource_payload)
#     assert create_resp["id"] > 0
#     assert create_resp["name"] == ds_name
#
#     ds_id = create_resp["id"]
#
#     # --- GET ---
#     get_resp = grafana_request("GET", f"/api/datasources/{ds_id}")
#     assert get_resp["id"] == ds_id
#     assert get_resp["name"] == ds_name
#     assert get_resp["type"] == "prometheus"
#
#     # --- UPDATE ---
#     updated_name = f"MyPrometheus-{uuid.uuid4().hex[:6]}"
#     update_payload = {
#         "id": ds_id,
#         "orgId": 1,  # usually the current org
#         "name": updated_name,
#         "type": "prometheus",
#         "access": "proxy",
#         "url": "http://prometheus:9090",
#         "isDefault": False,
#         "jsonData": {}
#     }
#     update_resp = grafana_request("PUT", f"/api/datasources/{ds_id}", json=update_payload)
#     assert update_resp["name"] == updated_name
#
#     # --- DELETE ---
#     delete_resp = grafana_request("DELETE", f"/api/datasources/{ds_id}")
#     # Grafana DELETE API returns an empty dict on success
#     assert delete_resp["message"] == "Data source deleted"
#
#     # --- VERIFY DELETION ---
#     with pytest.raises(Exception):
#         grafana_request("GET", f"/api/datasources/{ds_id}")
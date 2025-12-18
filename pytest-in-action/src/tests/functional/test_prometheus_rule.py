# import requests
# import pytest

# from src.fixtures.prometheus_fixtures import prometheus_url
# from src.fixtures.prometheus_fixtures import prometheus_rule_context


# @pytest.mark.functional
# @pytest.mark.prometheus
# class TestPrometheusRules:
#     def test_rules_loaded(self, prometheus_url):
#         resp = requests.get(f"{prometheus_url}/api/v1/rules")
#         assert resp.status_code == 200
#         data = resp.json()["data"]["groups"]
#         assert data == []

#     def test_recording_rule_present(self, prometheus_url, prometheus_rule_context):
#         ts = prometheus_rule_context["timestamp"]
#         resp = requests.get(f"{prometheus_url}/api/v1/rules")
#         assert resp.status_code == 200

#         groups = resp.json()["data"]["groups"]
#         records = [
#             r["name"]
#             for g in groups
#             for r in g["rules"]
#             if r["type"] == "recording"
#         ]

#         assert any(ts in r for r in records)

#     def test_alert_rule_present(self, prometheus_url, prometheus_rule_context):
#         ts = prometheus_rule_context["timestamp"]

#         resp = requests.get(f"{prometheus_url}/api/v1/rules")
#         groups = resp.json()["data"]["groups"]

#         alerts = [
#             r["name"]
#             for g in groups
#             for r in g["rules"]
#             if r["type"] == "alerting"
#         ]

#         assert any(ts in a for a in alerts)
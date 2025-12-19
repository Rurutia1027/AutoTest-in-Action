import requests
import pytest

from src.fixtures.prometheus_fixtures import prometheus_url


@pytest.mark.functional
@pytest.mark.prometheus
class TestPrometheusRules:

    def test_recording_rules_present(self, prometheus_url):
        resp = requests.get(f"{prometheus_url}/api/v1/rules")
        assert resp.status_code == 200

        groups = resp.json()["data"]["groups"]
        recording_rules = {
            r["name"] for g in groups if g["name"] == "test_recording_group"
            for r in g["rules"] if r["type"] == "recording"
        }

        assert "test_pg_connections" in recording_rules, "Recording rule test_pg_connections not found"

    def test_alerting_rules_present(self, prometheus_url):
        resp = requests.get(f"{prometheus_url}/api/v1/rules")
        assert resp.status_code == 200

        groups = resp.json()["data"]["groups"]
        alerting_rules = {
            r["name"] for g in groups if g["name"] == "test_alert_group"
            for r in g["rules"] if r["type"] == "alerting"
        }

        assert "TestPostgresConnectionsHigh" in alerting_rules, "Alerting rule TestPostgresConnectionsHigh not found"

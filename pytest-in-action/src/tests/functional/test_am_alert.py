# tests/alertmanager/test_am_alert.py
import datetime
import pytest
from datetime import datetime, timezone
from src.fixtures.am_fixtures import am_request


@pytest.mark.functional
@pytest.mark.alertmanager
class TestAlertmanagerAlert:
    def test_create_list_delete_alert(self, am_request):
        alert = [{
            "labels": {
                "alertname": "TestHighCPU",
                "severity": "warning",
                "service": "test-service"
            },
            "annotations": {},
            "startsAt": datetime.now(timezone.utc).isoformat()
        }]

        # Create
        am_request("POST", "/api/v2/alerts", json=alert)

        # List
        alerts = am_request("GET", "/api/v2/alerts", json=alert)
        names = [a["labels"]["alertname"] for a in alerts]

        assert "TestHighCPU" in names
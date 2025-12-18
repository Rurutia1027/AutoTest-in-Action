# tests/alertmanager/test_am_silence.py
import pytest
from datetime import datetime, timedelta
from src.fixtures.am_fixtures import am_request


@pytest.mark.functional
@pytest.mark.alertmanager
class TestAlertmanagerSilences:
    """Test CRUD operations for Alertmanager silences"""

    def test_create_list_delete_silence(self, am_request):
        now = datetime.utcnow()

        # Create a silence
        silence = {
            "matchers": [
                {"name": "service", "value": "test-service", "isRegex": False},
                {"name": "severity", "value": "critical", "isRegex": False},
            ],
            "startsAt": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "endsAt": (now + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "createdBy": "pytest",
            "comment": "temporary test silence"
        }

        created = am_request("POST", "api/v2/silences", json=silence)
        silence_id = created["silenceID"]
        assert silence_id

        # Verify silence exists
        silences = am_request("GET", "api/v2/silences")
        assert any(s["id"] == silence_id for s in silences)

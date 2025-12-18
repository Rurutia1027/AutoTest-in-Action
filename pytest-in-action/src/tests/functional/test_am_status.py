# tests/alertmanager/test_am_status.py

import pytest
from src.fixtures.am_fixtures import am_request

@pytest.mark.functional
@pytest.mark.alertmanager
class TestAlertmanagerStatus:

    def test_cluster_status(self, am_request):
        resp = am_request("GET", "api/v2/status")
        assert resp["cluster"]["status"] == "ready"
        assert "name" in resp["cluster"]
        assert "peers" in resp["cluster"]

    def test_version_info(self, am_request):
        resp = am_request("GET", "api/v2/status")
        assert "versionInfo" in resp
        assert "version" in resp["versionInfo"]

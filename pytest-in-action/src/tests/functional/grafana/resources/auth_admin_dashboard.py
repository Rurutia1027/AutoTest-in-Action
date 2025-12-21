import uuid
import pytest
from requests import HTTPError

from src.fixtures.grafana_fixtures import auth_admin_ctx, grafana_contexts, grafana_org_id, root_admin_ctx

@pytest.mark.functional
@pytest.mark.grafana
def test_admin_dashboard_crud(auth_admin_ctx):
    title = f"rbac-dashboard-test-{uuid.uuid4().hex[:6]}"
    dashboard = auth_admin_ctx.request(
        "POST",
        "/api/dashboards/db",
        json={
            "dashboard": {"title": title, "panels": [], "schemaVersion": 27},
            "overwrite": True
        }
    )
    uid = dashboard["uid"]

    # Fetch
    fetched = auth_admin_ctx.request("GET", f"/api/dashboards/uid/{uid}")
    assert fetched["dashboard"]["title"] == title

    # Update
    new_title = f"{title}-update"
    auth_admin_ctx.request(
        "POST",
        "/api/dashboards/db",
        json={
            "dashboard": {"title": new_title, "uid": uid, "panels": [], "schemaVersion": 27},
            "overwrite": True
        }
    )

    # Delete
    auth_admin_ctx.request("DELETE", f"/api/dashboards/uid/{uid}")

    # Verify deletion
    with pytest.raises(HTTPError) as excinfo:
        auth_admin_ctx.request("GET", f"/api/dashboards/uid/{uid}")

    # Assert 404 Not Found
    assert excinfo.value.response.status_code == 404


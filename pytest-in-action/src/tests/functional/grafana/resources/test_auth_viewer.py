import pytest
import uuid
from requests import HTTPError
from src.fixtures.grafana_fixtures import auth_viewer_ctx, auth_admin_ctx


@pytest.mark.functional
@pytest.mark.grafana
@pytest.mark.viewer
@pytest.mark.folder
def test_viewer_folder_crud(auth_viewer_ctx, auth_admin_ctx):
    # Admin creates a folder
    folder_title = f"viewer-folder-{uuid.uuid4().hex[:6]}"
    folder = auth_admin_ctx.request("POST", "/api/folders", json={"title": folder_title})
    folder_uid = folder["uid"]

    # Viewer fetches folder
    fetched = auth_viewer_ctx.request("GET", f"/api/folders/{folder_uid}")
    assert fetched["title"] == folder_title
    print("Folder Permissions (viewer):", fetched.get("canAdmin"), fetched.get("canEdit"), fetched.get("canDelete"))

    # Viewer cannot update
    with pytest.raises(HTTPError) as excinfo:
        auth_viewer_ctx.request("PUT", f"/api/folders/{folder_uid}", json={"title": f"{folder_title}-update", "version": fetched["version"]})
    assert excinfo.value.response.status_code in (403, 412)

    # Viewer cannot delete
    with pytest.raises(HTTPError) as excinfo:
        auth_viewer_ctx.request("DELETE", f"/api/folders/{folder_uid}", params={"version": fetched["version"]})
    assert excinfo.value.response.status_code == 403


@pytest.mark.functional
@pytest.mark.grafana
@pytest.mark.viewer
@pytest.mark.datasource
def test_viewer_datasource_read(auth_viewer_ctx, auth_admin_ctx):
    # Admin creates a datasource
    ds_name = f"admin-ds-{uuid.uuid4().hex[:6]}"
    ds = auth_admin_ctx.request("POST", "/api/datasources",
                                json={"name": ds_name, "type": "prometheus", "url": "http://prometheus:9090", "access": "proxy"})
    ds_id = ds["id"]

    # Viewer can read
    fetched = auth_viewer_ctx.request("GET", f"/api/datasources/{ds_id}")
    assert fetched["name"] == ds_name
    print("Datasource Permissions (viewer):", fetched.get("canAdmin"), fetched.get("canEdit"), fetched.get("canDelete"))

    # Viewer cannot create
    with pytest.raises(HTTPError) as excinfo:
        auth_viewer_ctx.request("POST", "/api/datasources", json={"name": f"viewer-ds-{uuid.uuid4().hex[:6]}", "type": "prometheus"})
    assert excinfo.value.response.status_code in (400, 403)

    # Viewer cannot delete
    with pytest.raises(HTTPError) as excinfo:
        auth_viewer_ctx.request("DELETE", f"/api/datasources/{ds_id}")
    assert excinfo.value.response.status_code == 403

    # Clean up
    auth_admin_ctx.request("DELETE", f"/api/datasources/{ds_id}")


@pytest.mark.functional
@pytest.mark.grafana
@pytest.mark.viewer
def test_viewer_rbac_observation(auth_viewer_ctx, auth_admin_ctx):
    """
    Observes Viewer permissions on folders and dashboards
    """

    # Admin creates folder & dashboard
    folder_title = f"rbac-folder-test-{uuid.uuid4().hex[:6]}"
    folder = auth_admin_ctx.request("POST", "/api/folders", json={"title": folder_title})
    folder_uid = folder["uid"]

    dashboard_title = f"rbac-dashboard-test-{uuid.uuid4().hex[:6]}"
    dashboard_payload = {
        "dashboard": {"title": dashboard_title, "panels": []},
        "folderId": folder["id"],
        "overwrite": False
    }
    dashboard = auth_admin_ctx.request("POST", "/api/dashboards/db", json=dashboard_payload)
    dashboard_uid = dashboard["uid"]

    # Viewer fetches folder & dashboard
    fetched_folder = auth_viewer_ctx.request("GET", f"/api/folders/{folder_uid}")
    fetched_dashboard = auth_viewer_ctx.request("GET", f"/api/dashboards/uid/{dashboard_uid}")

    print("Folder Permissions (viewer):", fetched_folder.get("canAdmin"), fetched_folder.get("canEdit"), fetched_folder.get("canDelete"))
    print("Dashboard Permissions (viewer):", fetched_dashboard["dashboard"].get("canAdmin"),
          fetched_dashboard["dashboard"].get("canEdit"), fetched_dashboard["dashboard"].get("canDelete"))

    # Viewer cannot update dashboard
    dashboard_payload["dashboard"]["title"] = f"{dashboard_title}-update"
    dashboard_payload["dashboard"]["version"] = fetched_dashboard["dashboard"]["version"]
    with pytest.raises(HTTPError) as excinfo:
        auth_viewer_ctx.request("POST", "/api/dashboards/db", json=dashboard_payload)
    assert excinfo.value.response.status_code in (403, 412)

    # Viewer cannot delete dashboard
    with pytest.raises(HTTPError) as excinfo:
        auth_viewer_ctx.request("DELETE", f"/api/dashboards/uid/{dashboard_uid}")
    assert excinfo.value.response.status_code == 403

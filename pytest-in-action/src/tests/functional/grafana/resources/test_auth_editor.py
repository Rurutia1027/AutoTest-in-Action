import pytest
import uuid
from requests import HTTPError
from src.fixtures.grafana_fixtures import auth_editor_ctx, grafana_contexts, grafana_org_id


@pytest.mark.functional
@pytest.mark.grafana
@pytest.mark.editor
@pytest.mark.folder
def test_editor_folder_crud(auth_editor_ctx):
    # Editor creates its own folder
    folder_title = f"editor-folder-{uuid.uuid4().hex[:6]}"
    folder = auth_editor_ctx.request("POST", "/api/folders", json={"title": folder_title})
    uid = folder["uid"]

    # Fetch
    fetched = auth_editor_ctx.request("GET", f"/api/folders/{uid}")
    version = fetched["version"]
    assert fetched["title"] == folder_title

    # Update allowed
    updated_title = f"{folder_title}-update"
    auth_editor_ctx.request("PUT", f"/api/folders/{uid}", json={"title": updated_title, "version": version})

    # Delete allowed (ownership)
    auth_editor_ctx.request("DELETE", f"/api/folders/{uid}", params={"version": version})

    # Verify deletion
    with pytest.raises(HTTPError) as excinfo:
        auth_editor_ctx.request("GET", f"/api/folders/{uid}")
    assert excinfo.value.response.status_code == 404


@pytest.mark.functional
@pytest.mark.grafana
@pytest.mark.editor
@pytest.mark.datasource
def test_editor_cannot_create_datasource(auth_editor_ctx):
    ds_name = f"editor-ds-{uuid.uuid4().hex[:7]}"
    with pytest.raises(HTTPError) as excinfo:
        auth_editor_ctx.request(
            "POST",
            "/api/datasources",
            json={"name": ds_name, "type": "prometheus"}
        )
    # Assert forbidden / bad request
    assert excinfo.value.response.status_code in (400, 403)


@pytest.mark.functional
@pytest.mark.grafana
@pytest.mark.editor
@pytest.mark.datasource
def test_editor_datasource_crud(auth_editor_ctx, auth_admin_ctx):
    ds_name = f"admin-ds-{uuid.uuid4().hex[:6]}"
    ds = auth_admin_ctx.request("POST", "/api/datasources",
                                json={"name": ds_name, "type": "prometheus", "url": "http://prometheus:9090",
                                      "access": "proxy"})
    ds_id = ds["id"]

    # Editor Role SA-Token only allowed to read the datasource
    fetched = auth_editor_ctx.request("GET", f"/api/datasources/{ds_id}")
    assert fetched["name"] == ds_name

    # Editor cannot delete - verify forbidden
    with pytest.raises(HTTPError) as excinfo:
        auth_editor_ctx.request("DELETE", f"/api/datasources/{ds_id}")
    assert excinfo.value.response.status_code == 403

    # Editor cannot create new datasource - verify forbidden
    with pytest.raises(HTTPError) as excinfo:
        auth_editor_ctx.request("POST", "/api/datasources",
                                json={"name": f"editor-ds-{uuid.uuid4().hex[:6]}", "type": "prometheus"})
    assert excinfo.value.response.status_code == 403

    # Optional: Editor can update if allowed
    # update_name = f"{ds_name}-update"
    # auth_editor_ctx.request("PUT", f"/api/datasources/{ds_id}", json={"name": update_name, "type": "prometheus", "version": fetched["version"]})

    # Clean up with Admin
    auth_admin_ctx.request("DELETE", f"/api/datasources/{ds_id}")

@pytest.mark.functional
@pytest.mark.grafana
@pytest.mark.editor
def test_editor_rbac_observation(auth_editor_ctx, auth_admin_ctx):
    """
    This test observes permission enforcement for Editor role.
    Logs canAdmin, canEdit, canDelete flags and captures what operations succeed/fail.
    """

    # Step 1: Admin creates a folder
    folder_title = f"rbac-folder-test-{uuid.uuid4().hex[:6]}"
    folder = auth_admin_ctx.request(
        "POST",
        "/api/folders",
        json={"title": folder_title}
    )
    folder_uid = folder["uid"]

    # Step 2: Admin creates a dashboard in that folder
    dashboard_title = f"rbac-dashboard-test-{uuid.uuid4().hex[:6]}"
    dashboard_payload = {
        "dashboard": {
            "title": dashboard_title,
            "panels": [],
        },
        "folderId": folder["id"],
        "overwrite": False
    }
    dashboard = auth_admin_ctx.request("POST", "/api/dashboards/db", json=dashboard_payload)
    dashboard_uid = dashboard["uid"]

    # Step 3: Editor fetches folder & dashboard
    fetched_folder = auth_editor_ctx.request("GET", f"/api/folders/{folder_uid}")
    fetched_dashboard = auth_editor_ctx.request("GET", f"/api/dashboards/uid/{dashboard_uid}")

    print("Folder Permissions:", fetched_folder.get("canAdmin"), fetched_folder.get("canEdit"),
          fetched_folder.get("canDelete"))
    print("Dashboard Permissions:", fetched_dashboard["dashboard"].get("canAdmin"),
          fetched_dashboard["dashboard"].get("canEdit"),
          fetched_dashboard["dashboard"].get("canDelete"))

    # Step 4: Editor tries to update dashboard
    dashboard_payload["dashboard"]["title"] = f"{dashboard_title}-update"
    dashboard_payload["dashboard"]["version"] = fetched_dashboard["dashboard"]["version"]
    try:
        updated_dashboard = auth_editor_ctx.request("POST", "/api/dashboards/db", json=dashboard_payload)
        print("Editor updated dashboard successfully")
    except HTTPError as e:
        print("Editor failed to update dashboard:", e.response.status_code)

    # Step 5: Editor tries to delete dashboard
    try:
        delete_resp = auth_editor_ctx.request("DELETE", f"/api/dashboards/uid/{dashboard_uid}")
        print("Editor deleted dashboard successfully")
    except HTTPError as e:
        print("Editor failed to delete dashboard:", e.response.status_code)
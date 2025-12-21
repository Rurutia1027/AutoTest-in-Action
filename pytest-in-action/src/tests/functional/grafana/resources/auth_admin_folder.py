import pytest
import uuid

from requests import HTTPError

from src.fixtures.grafana_fixtures import auth_admin_ctx, grafana_contexts, grafana_org_id, root_admin_ctx


@pytest.mark.functional
@pytest.mark.grafana
def test_admin_folder_crud(auth_admin_ctx):
    # Create
    folder_title = f"rbac-folder-test-{uuid.uuid4().hex[:6]}"
    folder = auth_admin_ctx.request(
        "POST",
        "/api/folders",
        json={"title": folder_title}
    )

    uid = folder["uid"]

    # Fetch
    fetched = auth_admin_ctx.request(
        "GET",
        f"/api/folders/{uid}"
    )

    version = fetched["version"]

    assert fetched["title"] == folder_title

    # Update
    folder_update_title = f"rbac-folder-update-test-{uuid.uuid4().hex[:6]}"
    auth_admin_ctx.request(
        "PUT",
        f"/api/folders/{uid}",
        json={"title": folder_update_title, "version": version}
    )

    # Delete
    auth_admin_ctx.request(
        "DELETE",
        f"/api/folders/{uid}",
        params={"version": fetched["version"]}
    )

    # Verify deletion
    with pytest.raises(HTTPError) as excinfo:
        auth_admin_ctx.request("GET", f"/api/folders/{uid}")

    # Assert 404 Not Found
    assert excinfo.value.response.status_code == 404

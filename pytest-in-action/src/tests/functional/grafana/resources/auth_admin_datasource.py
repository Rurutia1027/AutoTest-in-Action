import uuid

import pytest
from requests import HTTPError

from src.fixtures.grafana_fixtures import auth_admin_ctx, grafana_contexts, grafana_org_id, root_admin_ctx


@pytest.mark.functional
@pytest.mark.grafana
def test_admin_datasource_crud(auth_admin_ctx):
    name = f"rbac-datasource-{uuid.uuid4().hex[:6]}"
    ds = auth_admin_ctx.request(
        "POST",
        "/api/datasources",
        json={"name": name, "type": "prometheus", "url": "http://prometheus:9090", "access": "proxy"}
    )
    ds_id = ds["id"]

    # Fetch
    fetched = auth_admin_ctx.request("GET", f"/api/datasources/{ds_id}")
    assert fetched["name"] == name
    version = fetched["version"]
    assert version != ""

    # Update
    new_name = f"{name}-update-{uuid.uuid4().hex[:6]}"
    auth_admin_ctx.request("PUT", f"/api/datasources/{ds_id}", json={
        "name": new_name,
        "type": "prometheus",  # must match the type of the existing datasource
        "access": "proxy",  # must match existing
        "url": "http://prometheus:9090",  # must match existing or new valid value
        "isDefault": False,  # optional if not default
        "jsonData": {},
        "version": version
    })

    # Delete
    auth_admin_ctx.request("DELETE", f"/api/datasources/{ds_id}")

    # Verify deletion
    with pytest.raises(HTTPError) as excinfo:
        auth_admin_ctx.request("GET", f"/api/datasources/{ds_id}")

    # Assert 404 Not Found
    assert excinfo.value.response.status_code == 404

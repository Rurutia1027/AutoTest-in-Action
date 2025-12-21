import os
import pytest
import uuid
import requests

from dotenv import load_dotenv

load_dotenv()

GRAFANA_URL = os.environ.get("GRAFANA_URL")
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")


@pytest.fixture(scope="session")
def root_admin_ctx():
    return RootGrafanaContext(
        base_url=GRAFANA_URL,
        admin_user=ADMIN_USER,
        admin_password=ADMIN_PASSWORD
    )


@pytest.fixture(scope="session")
def grafana_org_id(root_admin_ctx):
    org = root_admin_ctx.request(
        "POST",
        "/api/orgs",
        json={"name": f"rbac-test-org-{uuid.uuid4().hex[:6]}"}
    )

    org_id = org["orgId"]
    resp = root_admin_ctx.request(
        "POST",
        f"/api/user/using/{org_id}",
    )

    assert resp['message'] == 'Active organization changed'

    return org_id


@pytest.fixture(scope="session")
def grafana_contexts(root_admin_ctx, grafana_org_id):
    contexts = {}

    for role in ["Admin", "Editor", "Viewer"]:
        sa = root_admin_ctx.request(
            "POST",
            "/api/serviceaccounts",
            json={"name": f"sa-{role.lower()}", "role": role}
        )

        token = root_admin_ctx.request(
            "POST",
            f"/api/serviceaccounts/{sa['id']}/tokens",
            json={
                "name": f"rbac-token-{role}-{uuid.uuid4().hex[:6]}",
                "secondsToLive": 0
            }
        )

        contexts[role] = GrafanaContext(
            base_url=GRAFANA_URL,
            token=token["key"],
            role=role,
            org_id=grafana_org_id,
        )

    return contexts


@pytest.fixture(scope="session")
def auth_admin_ctx(grafana_contexts):
    return grafana_contexts["Admin"]


@pytest.fixture(scope="session")
def auth_editor_ctx(grafana_contexts):
    return grafana_contexts["Editor"]


@pytest.fixture(scope="session")
def auth_viewer_ctx(grafana_contexts):
    return grafana_contexts["Viewer"]


# Root Grafana Context & Root User/Password Auth Context Holder
class RootGrafanaContext:
    def __init__(self, base_url, admin_user, admin_password):
        self.base_url = base_url
        self.admin_user = admin_user
        self.admin_password = admin_password
        self.auth = (self.admin_user, self.admin_password)

    def request(self, method, path, **kwargs):
        resp = requests.request(
            method,
            f"{self.base_url}/{path.lstrip('/')}",
            auth=self.auth,
            headers={"Content-Type": "application/json"},
            **kwargs
        )
        resp.raise_for_status()
        return resp.json() if resp.text else None


# Grafana Context & SA Token Holder
class GrafanaContext:
    def __init__(self, base_url, token, role, org_id):
        self.base_url = base_url
        self.token = token
        self.role = role
        self.org_id = org_id

    def request(self, method, path, **kwargs):
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.token}"

        resp = requests.request(method, f"{self.base_url.rstrip('/')}/{path.lstrip('/')}", headers=headers, **kwargs)

        if resp.status_code >= 400:
            resp.raise_for_status()
        return resp.json() if resp.text else None

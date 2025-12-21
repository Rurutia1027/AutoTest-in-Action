import os
import pytest

from dotenv import load_dotenv

from contexts.grafana_context import GrafanaContext

# load env variables
load_dotenv()

GRAFANA_URL = os.environ.get("GRAFANA_URL")


@pytest.fixture(scope="session")
def grafana_org(root_admin_ctx):
    org = root_admin_ctx.request(
        "POST",
        "/api/orgs",
        json={"name": "rbac-test-org"}
    )

    root_admin_ctx.request(
        "POST",
        f"/api/user/using/{org['id']}"
    )
    return org[id]


@pytest.fixture(scope="session")
def grafana_contexts(root_admin_ctx, grafana_org):
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
            json={"name": "rbac", "secondsToLive": 0}
        )
        contexts[role] = GrafanaContext(
            GRAFANA_URL, token["key"], role, grafana_org
        )
    return contexts

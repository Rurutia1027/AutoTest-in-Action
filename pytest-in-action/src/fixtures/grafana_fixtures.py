import os
import pytest

from dotenv import load_dotenv

from src.fixtures.grafana_bootstrap import GrafanaContext

# load env variables
load_dotenv()

GRAFANA_URL = os.environ.get("GRAFANA_URL")
GRAFANA_TOKEN = os.environ.get("GRAFANA_TOKEN")


@pytest.fixture(scope="session")
def grafana_context():
    base_url = os.getenv("GRAFANA_URL", "http://localhost:3000")
    admin_user = os.getenv("GRAFANA_ADMIN_USER", "admin")
    admin_password = os.getenv("GRAFANA_ADMIN_PASS", "admin")

    return GrafanaContext(base_url=base_url, admin_user=admin_user, admin_password=admin_password)


@pytest.fixture
def grafana_request(grafana_context: GrafanaContext):
    return grafana_context.request

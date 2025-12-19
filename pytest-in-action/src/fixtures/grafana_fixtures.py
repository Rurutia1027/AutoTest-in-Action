import os

from dotenv import load_dotenv

# load env variables
load_dotenv()

GRAFANA_URL = os.environ.get("GRAFANA_URL")
GRAFANA_TOKEN = os.environ.get("GRAFANA_TOKEN")

@pytest.fixture(scope="session")
def grafana_request():
    grafana_url = GRAFANA_URL
    grafana_token =

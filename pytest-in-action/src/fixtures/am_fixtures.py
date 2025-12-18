# src/fixtures/am_fixtures.py

import os
import requests
import pytest
from dotenv import load_dotenv

# load env variables
load_dotenv()

ALERTMANAGER_URL = os.environ.get('ALERTMANAGER_URL')


@pytest.fixture(scope="session")
def alertmanager_url():
    return ALERTMANAGER_URL


@pytest.fixture(scope="session")
def am_request():
    def _request(method, path, **kwargs):
        url = f"{ALERTMANAGER_URL.rstrip('/')}/{path.lstrip('/')}"
        try:
            r = requests.request(method, url, **kwargs)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP {e.response.status_code}: {e.response.text}")
        return r.json() if r.text else None
    return _request

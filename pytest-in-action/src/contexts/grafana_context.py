import requests
from dataclasses import dataclass
from typing import Optional, Dict, Any


class GrafanaContext:
    def __init__(self, base_url, token, role, org_id):
        self.base_url = base_url
        self.token = token
        self.role = role
        self.org_id = org_id

    def request(self, method, path, **kwargs):
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.token}"

        resp = requests.request(method, f"{self.base_url}{path}", headers=headers, **kwargs)

        if resp.status_code >= 400:
            resp.raise_for_status()
        return resp.json() if resp.text else None
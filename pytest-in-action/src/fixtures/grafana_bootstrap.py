import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class GrafanaContext:
    base_url: str
    admin_user: str = "admin"
    admin_password: str = "admin"

    def request(self, method: str, path: str, **kwargs):
        """
        Generic Grafana API requester using basic auth.
        """
        headers = kwargs.get("headers", {})
        headers.setdefault("Content-Type", "application/json")

        resp = requests.request(
            method,
            f"{self.base_url}/{path.lstrip('/')}",
            auth=(self.admin_user, self.admin_password),
            headers=headers,
            **kwargs
        )
        resp.raise_for_status()
        return resp.json() if resp.text else None
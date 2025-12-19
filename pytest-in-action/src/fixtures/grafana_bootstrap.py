import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class GrafanaContext:
    base_url: str
    admin_user: str = "admin"
    admin_password: str = "admin"
    token: Optional[str] = None

    def bootstrap_token(self,
                        token_name: str = "pytest-bootstrap-token",
                        role: str = "Admin",
                        ttl_seconds: int = 3600) -> str:
        """
        Create an API token using admin basic auth.
        """
        url = f"{self.base_url}/api/auth/keys"
        resp = requests.post(url, auth=(self.admin_user, self.admin_password),
                             json={
                                 "name": token_name,
                                 "role": role,
                                 "secondsToLive": ttl_seconds,
                             })
        resp.raise_for_status()
        self.token = resp.json()["key"]
        return self.token

    def request(self, method: str, path: str, **kwargs):
        """
        Generic Grafana API requester with Bearer auth.
        """
        if not self.token:
            raise RuntimeError("Grafana token not initialized")
        headers = kwargs.pop("headers", {})
        headers.setdefault("Authorization", f"Bearer {self.token}")
        headers.setdefault("Content-Type", "application/json")

        resp = requests.request(
            method,
            f"{self.base_url}/{path.lstrip('/')}",
            headers=headers,
            **kwargs
        )
        resp.raise_for_status()
        return resp.json() if resp.text else None
import requests
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class GrafanaContext:
    base_url: str
    admin_user: str = "admin"
    admin_password: str = "admin"
    sa_token: Optional[str] = None  # optional Service Account token

    def request(self, method: str, path: str, **kwargs) -> Any:
        """
        Generic Grafana API requester using either basic auth or SA token.
        """
        headers: Dict[str, str] = kwargs.get("headers", {})
        headers.setdefault("Content-Type", "application/json")

        # if SA token is provided, then use the SA token as Bearer Token
        if self.sa_token:
            headers["Authorization"] = f"Bearer {self.sa_token}"
            auth = None
        else:
            auth = (self.admin_user, self.admin_password)

        resp = requests.request(
            method,
            f"{self.base_url}/{path.strip('/')}",
            auth=auth,
            headers=headers,
            **kwargs
        )

        resp.raise_for_status()
        return resp.json() if resp.text else None

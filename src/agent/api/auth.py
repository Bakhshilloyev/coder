"""Optional API token auth (stdlib only)."""

import os


def required_token() -> str | None:
    return os.environ.get("API_TOKEN") or None


def authorize(headers: dict) -> bool:
    token = required_token()
    if not token:
        return True
    auth = headers.get("authorization") or headers.get("Authorization")
    if not auth:
        return False
    return auth == f"Bearer {token}" or auth == token

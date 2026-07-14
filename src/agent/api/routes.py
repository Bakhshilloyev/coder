"""Route handlers for the HTTP API."""

import json

from ..runtime.logging import get_logger
from .auth import authorize
from .schemas import validate_chat, validate_run

logger = get_logger("agent.api")


class ApiHandlers:
    def __init__(self, agent_factory):
        self.agent_factory = agent_factory

    def handle(self, method: str, path: str, headers: dict, body: bytes) -> tuple:
        # (status, json_dict)
        if not authorize(headers):
            return 401, {"error": "unauthorized"}
        if path == "/health" and method == "GET":
            return 200, {"status": "ok", "service": "goat-ai-agent"}
        if path == "/v1/models" and method == "GET":
            return 200, {"models": self.agent_factory().models()}
        if path == "/v1/info" and method == "GET":
            return 200, self.agent_factory().info()
        if path == "/v1/chat" and method == "POST":
            payload = _parse(body)
            data, err = validate_chat(payload)
            if err:
                return 400, {"error": err}
            return 200, {"reply": self.agent_factory().chat(data["message"])}
        if path == "/v1/run" and method == "POST":
            payload = _parse(body)
            data, err = validate_run(payload)
            if err:
                return 400, {"error": err}
            return 200, self.agent_factory().run(data["goal"])
        return 404, {"error": "not found"}


def _parse(body: bytes) -> dict:
    try:
        return json.loads(body or b"{}")
    except ValueError:
        return {}

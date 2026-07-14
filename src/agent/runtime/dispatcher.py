"""Dispatcher: routes high-level intents to the right agent capability."""

from typing import Any, Dict

from ..core.agent import Agent


class Dispatcher:
    """Thin facade used by the CLI/API to call agent capabilities uniformly."""

    def __init__(self, agent: Agent):
        self.agent = agent

    def dispatch(self, intent: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if intent == "chat":
            return {"reply": self.agent.chat(payload.get("message", ""))}
        if intent == "run":
            return self.agent.run(payload.get("goal", ""))
        if intent == "models":
            return {"models": self.agent.models()}
        if intent == "info":
            return self.agent.info()
        return {"error": f"unknown intent: {intent}"}

"""Offline, dependency-free provider.

The local provider never contacts the network. It produces deterministic,
useful output so the agent remains operational on weak devices, in airplane
mode, or when no API key is available. It is also used as the planner/executor
fallback when remote providers are unavailable.
"""

import re
from typing import Dict, List

from .provider_base import BaseProvider

_CODE_HINTS = (
    r"\b(write|create|implement|refactor|fix|debug|function|class|script|code|program)\b"
)
_QUESTION_HINTS = r"\?$"


class LocalProvider(BaseProvider):
    name = "local"

    def available(self) -> bool:
        return True

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        last_user = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user = m.get("content", "")
                break
        return self._respond(last_user)

    def _respond(self, prompt: str) -> str:
        prompt = (prompt or "").strip()
        if not prompt:
            return "Hello! I am the offline Goat AI Agent. Ask me to write code, plan a task, or run a command."
        if re.search(_CODE_HINTS, prompt, re.IGNORECASE):
            return self._code_response(prompt)
        if re.search(_QUESTION_HINTS, prompt) or "explain" in prompt.lower():
            return self._explain_response(prompt)
        return self._generic_response(prompt)

    def _code_response(self, prompt: str) -> str:
        snippet = 'def solution():\n    """%s"""\n    # TODO: implement\n    return None' % (
            prompt[:80].replace('"', "'")
        )
        return (
            "OFFLINE MODE — no network/API key required.\n"
            "Here is a starter implementation:\n\n"
            f"```python\n{snippet}\n```\n\n"
            "Tip: set a provider (e.g. MODEL_PROVIDER=groq) with an API key for full LLM features."
        )

    def _explain_response(self, prompt: str) -> str:
        return (
            "OFFLINE MODE — concise explanation.\n\n"
            f"Your request: {prompt}\n\n"
            "Break the problem into inputs, processing steps, and expected output. "
            "Use the built-in tools (file, shell, web) to gather details, then act."
        )

    def _generic_response(self, prompt: str) -> str:
        return (
            "OFFLINE MODE — I received your task: '%s'.\n"
            "I can plan, run shell/file/web tools, and remember context via SQLite memory. "
            "Configure a remote provider for richer answers." % prompt[:120]
        )

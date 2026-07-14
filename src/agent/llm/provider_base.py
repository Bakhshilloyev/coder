"""Base class and shared HTTP utilities for LLM providers.

All providers expose a synchronous ``chat(messages, **kwargs) -> str`` method
and a ``complete(prompt, **kwargs) -> str`` convenience wrapper. Messages use
the OpenAI-style shape: ``[{"role": "system"|"user"|"assistant", "content": str}]``.

Only the Python standard library is used for HTTP so the engine runs on
Termux and 32-bit devices without extra dependencies.
"""

import json
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from ..runtime.errors import ProviderError
from ..runtime.logging import get_logger
from ..utils.json import to_json

logger = get_logger("agent.llm")


class BaseProvider(ABC):
    name = "base"

    def __init__(self, model: str = "", api_key: str = "", **kwargs):
        self.model = model
        self.api_key = api_key
        self.extra = kwargs

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        ...

    def complete(self, prompt: str, system: str = "", **kwargs) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return self.chat(messages, **kwargs)

    def available(self) -> bool:
        """Whether this provider is configured and usable."""
        return True


def http_post(
    url: str,
    payload: dict,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 60,
) -> dict:
    """POST *payload* as JSON to *url* and return parsed JSON."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace") if exc.fp else ""
        raise ProviderError(
            f"HTTP {exc.code} from {url}: {body[:500]}", status=exc.code
        )
    except urllib.error.URLError as exc:
        raise ProviderError(f"Network error contacting {url}: {exc.reason}")
    try:
        return json.loads(raw)
    except ValueError as exc:
        raise ProviderError(f"Invalid JSON response from {url}: {exc}")


def http_get(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, method="GET")
    req.add_header("Accept", "application/json")
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        raise ProviderError(f"HTTP {exc.code} from {url}", status=exc.code)
    except urllib.error.URLError as exc:
        raise ProviderError(f"Network error contacting {url}: {exc.reason}")
    return json.loads(raw)

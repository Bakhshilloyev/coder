"""Anthropic (Claude) provider."""

from typing import Dict, List

from .provider_base import BaseProvider, http_post


class AnthropicProvider(BaseProvider):
    name = "anthropic"
    base_url = "https://api.anthropic.com/v1/messages"

    def __init__(self, model: str = "claude-3-5-sonnet-latest", api_key: str = "", **kwargs):
        super().__init__(model=model, api_key=api_key, **kwargs)

    def available(self) -> bool:
        return bool(self.api_key)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        if not self.available():
            return "OFFLINE FALLBACK — ANTHROPIC_API_KEY is not configured."
        system = ""
        convo = []
        for m in messages:
            role = m.get("role")
            if role == "system":
                system += m.get("content", "") + "\n"
            elif role in ("user", "assistant"):
                convo.append({"role": role, "content": m.get("content", "")})
        payload = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 1024),
            "system": system.strip(),
            "messages": convo,
        }
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        data = http_post(self.base_url, payload, headers=headers, timeout=90)
        try:
            return data["content"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            from ..runtime.errors import ProviderError

            raise ProviderError(f"Unexpected Anthropic response: {exc}")

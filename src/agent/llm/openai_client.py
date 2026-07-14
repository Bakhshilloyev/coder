"""OpenAI-compatible provider (works for OpenAI, Groq, and generic endpoints)."""

from typing import Dict, List, Optional

from .provider_base import BaseProvider, http_post


class OpenAICompatibleProvider(BaseProvider):
    """A provider that speaks the OpenAI Chat Completions protocol."""

    name = "openai-compatible"
    base_url = "https://api.openai.com/v1"

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: str = "",
        base_url: Optional[str] = None,
        auth_header: str = "Authorization",
        auth_prefix: str = "Bearer",
        timeout: int = 90,
        **kwargs,
    ):
        super().__init__(model=model, api_key=api_key, **kwargs)
        self.base_url = (base_url or self.base_url).rstrip("/")
        self.auth_header = auth_header
        self.auth_prefix = auth_prefix
        self.timeout = timeout

    def available(self) -> bool:
        return bool(self.api_key)

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            prefix = f"{self.auth_prefix} " if self.auth_prefix else ""
            headers[self.auth_header] = f"{prefix}{self.api_key}"
        return headers

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        if not self.available():
            return (
                "OFFLINE FALLBACK — no API key set for the remote provider. "
                "Set the relevant API key environment variable to enable it."
            )
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.4),
            "max_tokens": kwargs.get("max_tokens", 1024),
            "stream": False,
        }
        url = f"{self.base_url}/chat/completions"
        data = http_post(url, payload, headers=self._headers(), timeout=self.timeout)
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            from ..runtime.errors import ProviderError

            raise ProviderError(f"Unexpected response shape from {url}: {exc}")

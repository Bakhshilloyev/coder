"""Custom / configurable API provider.

Reads connection details from environment variables so it can target any
OpenAI-compatible gateway:

- CUSTOM_API_URL            endpoint base, e.g. https://my.host/v1
- CUSTOM_API_KEY            API key (optional)
- CUSTOM_API_MODEL          model name to send
- CUSTOM_API_AUTH_HEADER    header name (default: Authorization)
- CUSTOM_API_AUTH_PREFIX    token prefix (default: Bearer)
- CUSTOM_API_PROMPT_FIELD   request field for messages (default: messages)
- CUSTOM_API_MODEL_FIELD    request field for model (default: model)
- CUSTOM_API_RESPONSE_PATH  dotted path to the text in the response
"""

import os
from typing import Dict, List, Optional

from .openai_client import OpenAICompatibleProvider


class CustomProvider(OpenAICompatibleProvider):
    name = "custom"

    def __init__(self, model: str = "", api_key: str = "", base_url: str = "", **kwargs):
        self._prompt_field = os.environ.get("CUSTOM_API_PROMPT_FIELD", "messages")
        self._model_field = os.environ.get("CUSTOM_API_MODEL_FIELD", "model")
        self._response_path = os.environ.get("CUSTOM_API_RESPONSE_PATH", "choices.0.message.content")
        super().__init__(
            model=model or os.environ.get("CUSTOM_API_MODEL", ""),
            api_key=api_key or os.environ.get("CUSTOM_API_KEY", ""),
            base_url=base_url or os.environ.get("CUSTOM_API_URL", ""),
            auth_header=os.environ.get("CUSTOM_API_AUTH_HEADER", "Authorization"),
            auth_prefix=os.environ.get("CUSTOM_API_AUTH_PREFIX", "Bearer"),
            **kwargs,
        )

    def available(self) -> bool:
        return bool(self.base_url)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        if not self.available():
            return "OFFLINE FALLBACK — CUSTOM_API_URL is not configured."
        payload = {
            self._prompt_field: messages,
            self._model_field: self.model or "default",
            "temperature": kwargs.get("temperature", 0.4),
            "max_tokens": kwargs.get("max_tokens", 1024),
            "stream": False,
        }
        url = f"{self.base_url}/chat/completions"
        data = self._post(url, payload)
        # Navigate the configurable response path
        node = data
        for part in self._response_path.split("."):
            if part.isdigit():
                node = node[int(part)]
            else:
                node = node[part]
        return node

    def _post(self, url, payload) -> dict:
        from .provider_base import http_post

        return http_post(url, payload, headers=self._headers(), timeout=self.timeout)

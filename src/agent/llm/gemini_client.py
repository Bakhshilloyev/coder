"""Google Gemini provider."""

from typing import Dict, List
from urllib.parse import urlencode

from .provider_base import BaseProvider, http_post


class GeminiProvider(BaseProvider):
    name = "google"
    base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def __init__(self, model: str = "gemini-1.5-flash", api_key: str = "", **kwargs):
        super().__init__(model=model, api_key=api_key, **kwargs)

    def available(self) -> bool:
        return bool(self.api_key)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        if not self.available():
            return "OFFLINE FALLBACK — GEMINI_API_KEY is not configured."
        system = ""
        contents = []
        for m in messages:
            role = m.get("role")
            if role == "system":
                system += m.get("content", "") + "\n"
                continue
            grole = "model" if role == "assistant" else "user"
            contents.append({"role": grole, "parts": [{"text": m.get("content", "")}]})
        payload: Dict = {"contents": contents}
        if system.strip():
            payload["systemInstruction"] = {"parts": [{"text": system.strip()}]}
        url = f"{self.base_url}/{self.model}:generateContent?{urlencode({'key': self.api_key})}"
        data = http_post(url, payload, headers={"Content-Type": "application/json"}, timeout=90)
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            from ..runtime.errors import ProviderError

            raise ProviderError(f"Unexpected Gemini response: {exc}")

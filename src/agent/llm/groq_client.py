"""Groq provider (OpenAI-compatible)."""

from typing import Optional

from .openai_client import OpenAICompatibleProvider


class GroqProvider(OpenAICompatibleProvider):
    name = "groq"
    base_url = "https://api.groq.com/openai/v1"

    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",
        api_key: str = "",
        base_url: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            model=model,
            api_key=api_key,
            base_url=base_url or self.base_url,
            **kwargs,
        )

"""Provider/model registry.

Builds an LLM provider instance from configuration and environment variables.
Environment variables take precedence over config defaults.
"""

import os
from typing import Dict, List, Optional

from .anthropic_client import AnthropicProvider
from .custom_client import CustomProvider
from .gemini_client import GeminiProvider
from .groq_client import GroqProvider
from .local_client import LocalProvider
from .openai_client import OpenAICompatibleProvider
from .provider_base import BaseProvider

# Map a provider alias to (class, default-model, env-api-key-var)
_REGISTRY = {
    "local": (LocalProvider, "local", None),
    "openai": (OpenAICompatibleProvider, "gpt-4o-mini", "OPENAI_API_KEY"),
    "anthropic": (AnthropicProvider, "claude-3-5-sonnet-latest", "ANTHROPIC_API_KEY"),
    "claude": (AnthropicProvider, "claude-3-5-sonnet-latest", "ANTHROPIC_API_KEY"),
    "google": (GeminiProvider, "gemini-1.5-flash", "GEMINI_API_KEY"),
    "gemini": (GeminiProvider, "gemini-1.5-flash", "GEMINI_API_KEY"),
    "groq": (GroqProvider, "llama-3.3-70b-versatile", "GROQ_API_KEY"),
    "custom": (CustomProvider, "", "CUSTOM_API_KEY"),
}


def available_providers() -> List[str]:
    return list(_REGISTRY.keys())


def build_provider(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> BaseProvider:
    """Instantiate a provider by alias.

    Falls back to the offline ``local`` provider when no remote provider is
    configured, guaranteeing the agent always works.
    """
    provider = (provider or os.environ.get("MODEL_PROVIDER") or "local").lower()
    entry = _REGISTRY.get(provider)
    if not entry:
        # Unknown provider -> treat as custom OpenAI-compatible endpoint
        entry = (OpenAICompatibleProvider, provider, None)
        provider = "openai"

    cls, default_model, key_env = entry
    resolved_model = model or os.environ.get("MODEL_NAME") or default_model
    resolved_key = api_key or (os.environ.get(key_env) if key_env else "")

    try:
        instance = cls(model=resolved_model, api_key=resolved_key)  # type: ignore[call-arg]
    except Exception:
        instance = LocalProvider()

    if not instance.available() and not isinstance(instance, LocalProvider):
        # Degrade gracefully to offline mode instead of crashing.
        return LocalProvider()
    return instance


def list_models(config=None) -> List[Dict[str, str]]:
    """Return a human-readable list of configured models."""
    out: List[Dict[str, str]] = []
    if config is not None:
        for name, meta in (config.models or {}).items():
            out.append(
                {
                    "name": name,
                    "provider": meta.get("provider", "?"),
                    "best_for": ", ".join(meta.get("best_for", [])),
                }
            )
    return out

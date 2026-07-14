"""Error hierarchy for the agent runtime."""

from typing import Optional


class AgentError(Exception):
    """Base class for all agent errors."""


class ConfigError(AgentError):
    """Raised when configuration is missing or invalid."""


class ProviderError(AgentError):
    """Raised when an LLM provider call fails."""

    def __init__(self, message: str, provider: Optional[str] = None, status: Optional[int] = None):
        super().__init__(message)
        self.provider = provider
        self.status = status


class ToolError(AgentError):
    """Raised when a tool execution fails."""


class SafetyError(AgentError):
    """Raised when a policy guard blocks an action."""


class MemoryError(AgentError):
    """Raised when persistent memory operations fail."""

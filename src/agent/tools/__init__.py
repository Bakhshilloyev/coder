"""Tool framework: ``Tool`` definition, registry, and discovery helpers."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

# Global registry filled by the individual tool modules.
REGISTRY: Dict[str, "Tool"] = {}


@dataclass
class ToolResult:
    success: bool
    output: str
    error: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "meta": self.meta,
        }


class Tool:
    """A single callable tool the agent can route to."""

    def __init__(
        self,
        name: str,
        description: str,
        handler: Callable[..., ToolResult],
        parameters: Optional[List[Dict[str, str]]] = None,
        requires_confirmation: bool = False,
        category: str = "general",
    ):
        self.name = name
        self.description = description
        self.handler = handler
        self.parameters = parameters or []
        self.requires_confirmation = requires_confirmation
        self.category = category

    def run(self, **kwargs) -> ToolResult:
        return self.handler(**kwargs)

    def schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "requires_confirmation": self.requires_confirmation,
            "category": self.category,
        }


def register(tool: Tool) -> Tool:
    REGISTRY[tool.name] = tool
    return tool


def get_tool(name: str) -> Optional[Tool]:
    return REGISTRY.get(name)


def all_tools() -> List[Tool]:
    return list(REGISTRY.values())


def discover() -> List[Tool]:
    """Import tool modules (idempotent) so they register themselves."""
    import importlib
    from ..runtime.logging import get_logger

    logger = get_logger("agent.tools")
    for mod in (
        "agent.tools.file_tools",
        "agent.tools.shell_tools",
        "agent.tools.web_tools",
        "agent.tools.api_tools",
        "agent.tools.memory_tools",
        "agent.tools.db_tools",
    ):
        try:
            importlib.import_module(mod)
        except Exception as exc:  # pragma: no cover - optional deps
            logger.warning("Skipping tool module %s: %s", mod, exc)
    return all_tools()

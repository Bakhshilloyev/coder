"""Executor: runs routed tools and handles confirmation gates."""

import os
from typing import Callable, Optional

from ..runtime.errors import ToolError
from ..runtime.logging import get_logger
from ..tools import Tool, ToolResult
from .tool_router import Route, ToolRouter

logger = get_logger("agent.executor")


class Executor:
    def __init__(self, router: ToolRouter, confirm: Optional[Callable[[str], bool]] = None):
        self.router = router
        self.confirm = confirm

    def execute_request(self, request: str) -> Optional[ToolResult]:
        """Route and run *request*. Returns ``None`` when no tool matches."""
        route = self.router.route(request)
        if route.tool is None:
            return None
        return self.run_tool(route.tool, route.args)

    def run_tool(self, tool: Tool, args: dict) -> ToolResult:
        logger.info("executing tool=%s args=%s", tool.name, list(args))
        try:
            result = tool.run(**args)
        except Exception as exc:
            raise ToolError(f"{tool.name} failed: {exc}") from exc

        if result.error == "CONFIRMATION_REQUIRED":
            cmd = result.meta.get("command", "")
            approved = False
            if self.confirm is not None:
                approved = self.confirm(cmd)
            elif os.environ.get("AUTO_APPROVE_SHELL") == "1":
                approved = True
            if approved:
                os.environ["AUTO_APPROVE_SHELL"] = "1"
                result = tool.run(**args)
                os.environ.pop("AUTO_APPROVE_SHELL", None)
            else:
                return ToolResult(
                    False,
                    "",
                    error="Command requires confirmation and was not approved.",
                )
        return result

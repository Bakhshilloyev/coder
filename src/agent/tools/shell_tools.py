"""Shell execution tools with a safety gate.

Commands are screened by :mod:`agent.core.safety` before execution. Blocked
patterns (e.g. ``rm -rf /``) are never run. Interactive confirmation is
requested for mutating commands unless ``AUTO_APPROVE_SHELL=1``.
"""

import os
import subprocess

from . import Tool, ToolResult, register


def _safe_shell(command: str, timeout: int = 60, cwd: str = None) -> ToolResult:
    from ..core.safety import check_command

    verdict = check_command(command)
    if not verdict.allowed:
        return ToolResult(False, "", error=f"BLOCKED by safety policy: {verdict.reason}")

    if verdict.requires_confirmation and os.environ.get("AUTO_APPROVE_SHELL") != "1":
        return ToolResult(
            False,
            "",
            error="CONFIRMATION_REQUIRED",
            meta={"needs_confirmation": True, "command": command},
        )

    try:
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
        )
    except subprocess.TimeoutExpired:
        return ToolResult(False, "", error=f"Command timed out after {timeout}s")
    except Exception as exc:  # pragma: no cover
        return ToolResult(False, "", error=str(exc))

    out = (proc.stdout or "") + (proc.stderr or "")
    return ToolResult(
        proc.returncode == 0,
        out[:20000] or "(no output)",
        error=None if proc.returncode == 0 else f"exit code {proc.returncode}",
        meta={"returncode": proc.returncode},
    )


register(
    Tool(
        "shell_run",
        "Run a shell command (safety-filtered).",
        _safe_shell,
        [
            {"name": "command", "type": "string"},
            {"name": "timeout", "type": "int"},
            {"name": "cwd", "type": "string"},
        ],
        requires_confirmation=True,
        category="shell",
    )
)

"""Tool router: maps a natural-language request to the best tool + args."""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from ..runtime.logging import get_logger
from ..tools import Tool, all_tools, discover

logger = get_logger("agent.router")


@dataclass
class Route:
    tool: Optional[Tool]
    args: Dict
    reason: str


# Keyword -> (compiled pattern, tool name, arg key)
_RULES: List[Tuple[re.Pattern, str, str]] = [
    (re.compile(r"\b(read|show|cat|view)\b.*\b(\S+\.\w+|\S+)\b", re.I), "file_read", "path"),
    (re.compile(r"\b(list|ls|dir|files in)\b", re.I), "file_list", "path"),
    (re.compile(r"\b(search|grep|find)\b.*\b(in|under|files?)\b", re.I), "file_search", "pattern"),
    (re.compile(r"\b(write|create|save)\b.*\b(file|to)\b", re.I), "file_write", "path"),
    (re.compile(r"\b(fetch|download|open url|get url)\b", re.I), "web_fetch", "url"),
    (re.compile(r"\b(web search|search the web|google|duckduckgo)\b", re.I), "web_search", "query"),
    (re.compile(r"\b(run|execute|shell|command|cmd)\b", re.I), "shell_run", "command"),
    (re.compile(r"\b(call|request|http|api|post|get)\b.*\b(endpoint|url|api)\b", re.I), "api_call", "url"),
    (re.compile(r"\b(remember|store|save fact)\b", re.I), "memory_remember", "key"),
    (re.compile(r"\b(recall|what did i|retrieve)\b", re.I), "memory_recall", "key"),
    (re.compile(r"\b(query|sql|select)\b.*\b(database|db|\.db)\b", re.I), "db_query", "path"),
]


_PATH_TOKEN = re.compile(r"[\w./\\-]+\.\w+")
_QUOTED = re.compile(r'["\']([^"\']+)["\']')


class ToolRouter:
    def __init__(self):
        self.tools = {}
        self._ready = False

    def _ensure(self):
        if self._ready:
            return
        discover()
        self.tools = {t.name: t for t in all_tools()}
        self._ready = True

    def route(self, request: str) -> Route:
        self._ensure()
        for rx, tool_name, arg_key in _RULES:
            m = rx.search(request)
            if m and tool_name in self.tools:
                args = self._build_args(tool_name, request, m)
                return Route(self.tools[tool_name], args, f"matched: {rx.pattern[:30]}")
        return Route(None, {}, "no tool matched; will use LLM")

    def _build_args(self, tool_name: str, request: str, m) -> dict:
        if tool_name == "shell_run":
            return {"command": request}
        if tool_name == "file_list":
            return {"path": ".", "recursive": "recursive" in request.lower()}
        if tool_name == "memory_remember":
            text = re.sub(r"^\s*(remember|store|save fact)\b", "", request, flags=re.I).strip()
            if " is " in text:
                key, value = text.split(" is ", 1)
            else:
                key, value = "fact", text
            return {"key": key.strip(), "value": value.strip()}
        if tool_name == "memory_recall":
            text = re.sub(r"^\s*(recall|what (is|did i)|retrieve)\b", "", request, flags=re.I).strip()
            return {"key": text or "fact"}
        if tool_name in ("file_read", "file_write", "file_search"):
            path = _PATH_TOKEN.search(request)
            quoted = _QUOTED.search(request)
            value = (quoted.group(1) if quoted else None) or (path.group(0) if path else "")
            if tool_name == "file_search":
                # pattern is the search term (strip leading verbs)
                pat = quoted.group(1) if quoted else request.split("for", 1)[-1].strip()
                return {"pattern": pat, "path": "."}
            return {("path" if tool_name != "file_write" else "path"): value}
        # generic: use the last regex group as the argument
        arg = m.group(m.lastindex or 1).strip().strip('"').strip("'")
        return {_RULES_ARG(tool_name): arg}

    def list_tools(self) -> List[Dict]:
        self._ensure()
        return [t.schema() for t in self.tools.values()]


def _RULES_ARG(tool_name: str) -> str:
    return {
        "web_fetch": "url",
        "web_search": "query",
        "api_call": "url",
        "memory_remember": "key",
        "memory_recall": "key",
        "db_query": "path",
    }.get(tool_name, "input")

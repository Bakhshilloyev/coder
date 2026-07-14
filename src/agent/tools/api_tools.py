"""API tools: call arbitrary HTTP endpoints (GET/POST)."""

import json

from . import Tool, ToolResult, register
from ..llm.provider_base import http_get, http_post
from ..utils.json import try_parse_json


def api_call(
    url: str,
    method: str = "GET",
    headers: str = "{}",
    body: str = "",
    timeout: int = 30,
) -> ToolResult:
    try:
        hdr = json.loads(headers) if headers else {}
    except ValueError as exc:
        return ToolResult(False, "", error=f"Invalid headers JSON: {exc}")

    payload = None
    if body:
        payload = try_parse_json(body) if body.strip().startswith(("{", "[")) else body

    try:
        if method.upper() == "GET":
            data = http_get(url, headers=hdr, timeout=timeout)
        else:
            data = http_post(url, payload if payload is not None else {}, headers=hdr, timeout=timeout)
    except Exception as exc:
        return ToolResult(False, "", error=str(exc))
    return ToolResult(True, json.dumps(data, ensure_ascii=False)[:8000], meta={"url": url})


register(
    Tool(
        "api_call",
        "Call an HTTP endpoint (GET/POST) with optional JSON body/headers.",
        api_call,
        [
            {"name": "url", "type": "string"},
            {"name": "method", "type": "string"},
            {"name": "headers", "type": "string"},
            {"name": "body", "type": "string"},
        ],
        category="api",
    )
)

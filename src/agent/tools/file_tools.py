"""File system tools: read, write, list, search."""

import os
import re

from . import Tool, ToolResult, register
from ..utils.files import ensure_dir, list_files, read_text, safe_join, write_text


def file_read(path: str, limit: int = 8000) -> ToolResult:
    if not os.path.isfile(path):
        return ToolResult(False, "", error=f"File not found: {path}")
    return ToolResult(True, read_text(path, limit=int(limit)), meta={"path": path})


def file_write(path: str, content: str) -> ToolResult:
    n = write_text(path, content)
    return ToolResult(True, f"wrote {n} bytes to {path}", meta={"bytes": n})


def file_list(path: str = ".", recursive: bool = False) -> ToolResult:
    if not os.path.isdir(path):
        return ToolResult(False, "", error=f"Not a directory: {path}")
    items = list_files(path, recursive=bool(recursive))
    return ToolResult(True, "\n".join(items) or "(empty)", meta={"count": len(items)})


def file_search(path: str = ".", pattern: str = ".", ext: str = None) -> ToolResult:
    try:
        rx = re.compile(pattern)
    except re.error as exc:
        return ToolResult(False, "", error=f"Bad regex: {exc}")
    matches = []
    for fp in list_files(path, recursive=True, ext=ext):
        try:
            text = read_text(fp, limit=200_000)
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if rx.search(line):
                matches.append(f"{fp}:{i}: {line}")
    return ToolResult(True, "\n".join(matches[:200]) or "(no matches)", meta={"count": len(matches)})


register(
    Tool(
        "file_read",
        "Read a text file (returns up to `limit` chars).",
        file_read,
        [{"name": "path", "type": "string"}, {"name": "limit", "type": "int"}],
        category="file",
    )
)
register(
    Tool(
        "file_write",
        "Write text content to a file (creates parent dirs).",
        file_write,
        [{"name": "path", "type": "string"}, {"name": "content", "type": "string"}],
        requires_confirmation=True,
        category="file",
    )
)
register(
    Tool(
        "file_list",
        "List files in a directory.",
        file_list,
        [{"name": "path", "type": "string"}, {"name": "recursive", "type": "bool"}],
        category="file",
    )
)
register(
    Tool(
        "file_search",
        "Search files for a regex pattern and return matching lines.",
        file_search,
        [{"name": "path", "type": "string"}, {"name": "pattern", "type": "string"}, {"name": "ext", "type": "string"}],
        category="file",
    )
)

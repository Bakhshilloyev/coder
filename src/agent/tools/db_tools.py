"""Database tool: run a read-only SQL query against a SQLite file."""

import sqlite3

from . import Tool, ToolResult, register


def db_query(path: str, query: str, limit: int = 50) -> ToolResult:
    if not path.lower().endswith(".db") and not path.lower().endswith(".sqlite"):
        return ToolResult(False, "", error="Only SQLite (.db/.sqlite) files are supported")
    if not any(k in query.upper() for k in ("SELECT", "PRAGMA")):
        return ToolResult(False, "", error="Only SELECT/PRAGMA queries are allowed")
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query).fetchmany(int(limit))
        conn.close()
    except Exception as exc:
        return ToolResult(False, "", error=str(exc))
    out = [dict(r) for r in rows]
    return ToolResult(
        True,
        "\n".join(str(r) for r in out) or "(no rows)",
        meta={"rows": len(out)},
    )


register(
    Tool(
        "db_query",
        "Run a read-only SELECT/PRAGMA query on a SQLite database.",
        db_query,
        [
            {"name": "path", "type": "string"},
            {"name": "query", "type": "string"},
            {"name": "limit", "type": "int"},
        ],
        category="db",
    )
)

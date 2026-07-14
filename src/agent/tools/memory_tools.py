"""Memory tools: remember / recall facts in the durable store."""

from . import Tool, ToolResult, register
from ..memory.sqlite_store import SQLiteStore

_STORE: SQLiteStore | None = None


def init_memory(store: SQLiteStore) -> None:
    global _STORE
    _STORE = store


def memory_remember(key: str, value: str) -> ToolResult:
    if _STORE is None:
        return ToolResult(False, "", error="Memory store not initialised")
    _STORE.set(key, value)
    return ToolResult(True, f"remembered: {key}")


def memory_recall(key: str) -> ToolResult:
    if _STORE is None:
        return ToolResult(False, "", error="Memory store not initialised")
    val = _STORE.get(key)
    if val is None:
        return ToolResult(False, "", error=f"No memory for key: {key}")
    return ToolResult(True, val, meta={"key": key})


def memory_list() -> ToolResult:
    if _STORE is None:
        return ToolResult(False, "", error="Memory store not initialised")
    facts = _STORE.all()
    text = "\n".join(f"{k} = {v}" for k, v in facts.items()) or "(empty)"
    return ToolResult(True, text, meta={"count": len(facts)})


register(
    Tool(
        "memory_remember",
        "Store a key/value fact in long-term memory.",
        memory_remember,
        [{"name": "key", "type": "string"}, {"name": "value", "type": "string"}],
        category="memory",
    )
)
register(
    Tool(
        "memory_recall",
        "Recall a value previously stored by key.",
        memory_recall,
        [{"name": "key", "type": "string"}],
        category="memory",
    )
)
register(
    Tool(
        "memory_list",
        "List all stored memories.",
        memory_list,
        [],
        category="memory",
    )
)

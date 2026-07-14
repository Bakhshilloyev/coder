"""Short-term (in-process) and long-term memory abstractions."""

from typing import Dict, List

from .sqlite_store import SQLiteStore


class ShortTermMemory:
    """Rolling in-memory context window (bounded to save RAM on weak devices)."""

    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self.buffer: List[Dict] = []

    def add(self, role: str, content: str) -> None:
        self.buffer.append({"role": role, "content": content})
        if len(self.buffer) > self.max_turns:
            self.buffer = self.buffer[-self.max_turns :]

    def snapshot(self) -> List[Dict]:
        return list(self.buffer)

    def clear(self) -> None:
        self.buffer = []


class LongTermMemory:
    """Thin wrapper exposing the SQLite store as durable memory."""

    def __init__(self, store: SQLiteStore):
        self.store = store

    def remember(self, key: str, value: str) -> None:
        self.store.set(key, value)

    def recall(self, key: str):
        return self.store.get(key)

    def facts(self) -> Dict[str, str]:
        return self.store.all()

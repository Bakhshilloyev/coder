"""Long-term memory facade (backed by the SQLite store)."""

from .sqlite_store import SQLiteStore


class LongTermMemory:
    def __init__(self, store: SQLiteStore):
        self.store = store

    def remember(self, key: str, value: str) -> None:
        self.store.set(key, value)

    def recall(self, key: str):
        return self.store.get(key)

    def forget(self, key: str) -> None:
        self.store.delete(key)

    def dump(self) -> dict:
        return self.store.all()

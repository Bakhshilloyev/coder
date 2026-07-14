"""Agent-facing memory aggregator (core layer).

Combines short-term dialogue context, long-term key/value facts, and sessions
on top of the SQLite store. This is the single object the agent interacts with.
"""

from ..memory.sessions import SessionManager
from ..memory.short_term import ShortTermMemory
from ..memory.long_term import LongTermMemory
from ..memory.sqlite_store import SQLiteStore


class Memory:
    def __init__(self, db_path: str = "data/memory/agent.db", max_turns: int = 20):
        self.store = SQLiteStore(db_path)
        self.short_term = ShortTermMemory(max_turns=max_turns)
        self.long_term = LongTermMemory(self.store)
        self.sessions = SessionManager(self.store)
        self.session = self.sessions.create()

    def add_turn(self, role: str, content: str) -> None:
        self.short_term.add(role, content)
        self.session.add(role, content)

    def remember(self, key: str, value: str) -> None:
        self.long_term.remember(key, value)

    def recall(self, key: str):
        return self.long_term.recall(key)

    def context_messages(self, limit: int = 20) -> list:
        return self.short_term.snapshot()[-limit:]

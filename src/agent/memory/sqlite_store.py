"""Persistent memory backed by SQLite (stdlib, no extra deps)."""

import os
import sqlite3
import threading
from typing import Dict, List, Optional

from ..runtime.errors import MemoryError
from ..runtime.logging import get_logger

logger = get_logger("agent.memory")


class SQLiteStore:
    """A small key/value + event log store used for long-term memory."""

    def __init__(self, path: str = "data/memory/agent.db"):
        self.path = path
        if path:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self._lock = threading.Lock()
        self._init()

    def _connect(self) -> sqlite3.Connection:
        if not self.path:
            raise MemoryError("In-memory store requires a path")
        conn = sqlite3.connect(self.path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS kv ("
                "key TEXT PRIMARY KEY, value TEXT, updated INTEGER)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS events ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, session TEXT, kind TEXT, "
                "payload TEXT, ts INTEGER)"
            )

    # -- key/value -------------------------------------------------------
    def set(self, key: str, value: str) -> None:
        import time

        with self._lock, self._connect() as conn:
            conn.execute(
                "INSERT INTO kv(key, value, updated) VALUES(?,?,?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated=excluded.updated",
                (key, value, int(time.time())),
            )

    def get(self, key: str) -> Optional[str]:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT value FROM kv WHERE key=?", (key,)).fetchone()
        return row["value"] if row else None

    def delete(self, key: str) -> None:
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM kv WHERE key=?", (key,))

    def all(self) -> Dict[str, str]:
        with self._lock, self._connect() as conn:
            rows = conn.execute("SELECT key, value FROM kv").fetchall()
        return {r["key"]: r["value"] for r in rows}

    # -- event log -------------------------------------------------------
    def log_event(self, session: str, kind: str, payload: str) -> None:
        import time

        with self._lock, self._connect() as conn:
            conn.execute(
                "INSERT INTO events(session, kind, payload, ts) VALUES(?,?,?,?)",
                (session, kind, payload, int(time.time())),
            )

    def events(self, session: Optional[str] = None, limit: int = 100) -> List[Dict]:
        with self._lock, self._connect() as conn:
            if session:
                rows = conn.execute(
                    "SELECT * FROM events WHERE session=? ORDER BY id DESC LIMIT ?",
                    (session, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,)
                ).fetchall()
        return [dict(r) for r in rows]

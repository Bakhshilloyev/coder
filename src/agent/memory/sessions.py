"""Session management on top of the SQLite store."""

import uuid
from typing import Dict, List, Optional

from .sqlite_store import SQLiteStore


class Session:
    def __init__(self, session_id: str, store: SQLiteStore):
        self.id = session_id
        self.store = store
        self.turns: List[Dict] = []

    def add(self, role: str, content: str) -> None:
        turn = {"role": role, "content": content}
        self.turns.append(turn)
        self.store.log_event(self.id, role, content)

    def history(self, limit: int = 20) -> List[Dict]:
        return self.turns[-limit:]


class SessionManager:
    def __init__(self, store: SQLiteStore):
        self.store = store
        self._sessions: Dict[str, Session] = {}

    def create(self, session_id: Optional[str] = None) -> Session:
        sid = session_id or uuid.uuid4().hex[:12]
        if sid not in self._sessions:
            self._sessions[sid] = Session(sid, self.store)
        return self._sessions[sid]

    def get(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

    def list(self) -> List[str]:
        return list(self._sessions.keys())

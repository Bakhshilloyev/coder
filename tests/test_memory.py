import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent.memory.sqlite_store import SQLiteStore
from agent.memory.sessions import SessionManager


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = os.path.join(self.tmp, "m.db")
        self.store = SQLiteStore(self.db)

    def test_set_get(self):
        self.store.set("k", "v")
        self.assertEqual(self.store.get("k"), "v")

    def test_delete(self):
        self.store.set("k", "v")
        self.store.delete("k")
        self.assertIsNone(self.store.get("k"))

    def test_events(self):
        self.store.log_event("s1", "user", "hi")
        events = self.store.events(session="s1")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["payload"], "hi")

    def test_sessions(self):
        mgr = SessionManager(self.store)
        s = mgr.create("abc")
        s.add("user", "hello")
        self.assertEqual(len(mgr.get("abc").turns), 1)


if __name__ == "__main__":
    unittest.main()

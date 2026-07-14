import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent.core.executor import Executor
from agent.core.tool_router import ToolRouter


class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.router = ToolRouter()
        self.exec = Executor(self.router)

    def test_execute_file_list(self):
        res = self.exec.execute_request("list files in the current directory")
        self.assertIsNotNone(res)
        self.assertTrue(res.success)
        self.assertIn("pyproject.toml", res.output)

    def test_execute_unknown_returns_none(self):
        res = self.exec.execute_request("please tell me a joke about cats")
        self.assertIsNone(res)

    def test_shell_blocked_command(self):
        res = self.exec.execute_request("run rm -rf /")
        self.assertIsNotNone(res)
        self.assertFalse(res.success)
        self.assertIn("BLOCKED", res.error)


if __name__ == "__main__":
    unittest.main()

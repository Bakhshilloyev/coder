import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent.core.tool_router import ToolRouter


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.router = ToolRouter()

    def test_list_files(self):
        route = self.router.route("list files in the current directory")
        self.assertEqual(route.tool.name, "file_list")

    def test_fetch_url(self):
        route = self.router.route("fetch https://example.com")
        self.assertEqual(route.tool.name, "web_fetch")

    def test_search_web(self):
        route = self.router.route("search the web for python tips")
        self.assertEqual(route.tool.name, "web_search")

    def test_no_match(self):
        route = self.router.route("what is the meaning of life")
        self.assertIsNone(route.tool)


if __name__ == "__main__":
    unittest.main()

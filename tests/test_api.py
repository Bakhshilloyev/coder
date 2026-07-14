import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent.api.routes import ApiHandlers
from agent.api.auth import required_token


class FakeAgent:
    def chat(self, message):
        return f"echo: {message}"

    def models(self):
        return [{"name": "local", "provider": "local", "best_for": "offline"}]

    def info(self):
        return {"name": "test", "provider": "local"}

    def run(self, goal):
        return {"goal": goal, "summary": "done"}


class TestApi(unittest.TestCase):
    def setUp(self):
        self.handlers = ApiHandlers(lambda: FakeAgent())

    def test_health(self):
        status, payload = self.handlers.handle("GET", "/health", {}, b"")
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "ok")

    def test_models(self):
        status, payload = self.handlers.handle("GET", "/v1/models", {}, b"")
        self.assertEqual(status, 200)
        self.assertEqual(payload["models"][0]["name"], "local")

    def test_chat(self):
        status, payload = self.handlers.handle(
            "POST", "/v1/chat", {}, b'{"message": "hi"}'
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["reply"], "echo: hi")

    def test_chat_validation(self):
        status, payload = self.handlers.handle("POST", "/v1/chat", {}, b"{}")
        self.assertEqual(status, 400)

    def test_unknown(self):
        status, _ = self.handlers.handle("GET", "/nope", {}, b"")
        self.assertEqual(status, 404)

    def test_auth_required(self):
        os.environ["API_TOKEN"] = "secret"
        try:
            status, _ = self.handlers.handle("GET", "/health", {}, b"")
            self.assertEqual(status, 401)
            status, _ = self.handlers.handle(
                "GET", "/health", {"authorization": "Bearer secret"}, b""
            )
            self.assertEqual(status, 200)
        finally:
            os.environ.pop("API_TOKEN", None)


if __name__ == "__main__":
    unittest.main()

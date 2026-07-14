"""HTTP API server (stdlib only, no external framework)."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from ..app import get_agent
from .routes import ApiHandlers


def make_handler(handlers: ApiHandlers):
    class Handler(BaseHTTPRequestHandler):
        def _headers_dict(self):
            return {k.lower(): v for k, v in self.headers.items()}

        def do_GET(self):
            status, payload = handlers.handle("GET", self.path, self._headers_dict(), b"")
            self._respond(status, payload)

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0) or 0)
            body = self.rfile.read(length) if length else b""
            status, payload = handlers.handle("POST", self.path, self._headers_dict(), body)
            self._respond(status, payload)

        def _respond(self, status, payload):
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *args):
            pass

    return Handler


def run_server(host: str = "127.0.0.1", port: int = 8000, provider=None, model=None) -> None:
    handlers = ApiHandlers(lambda: get_agent(provider=provider, model=model))
    httpd = ThreadingHTTPServer((host, port), make_handler(handlers))
    print(f"Unified AI Agent API listening on http://{host}:{port}")
    print("Endpoints: /health /v1/models /v1/info /v1/chat /v1/run")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()

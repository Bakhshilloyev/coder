"""Command-line interface for the Unified AI Agent.

Examples
--------
    python -m agent.main models
    python -m agent.main info
    python -m agent.main chat "Hello"
    MODEL_PROVIDER=groq GROQ_API_KEY=... python -m agent.main run "List files in /tmp"
    python -m agent.main server --port 8000
"""

import argparse
import json
import sys

from .app import get_agent
from .runtime.logging import configure_logging, level_from_env
from .version import __version__


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agent", description="Unified Cross-Platform AI Agent")
    p.add_argument("--version", action="version", version=f"unified-ai-agent {__version__}")
    p.add_argument("--provider", default=None, help="LLM provider override (env: MODEL_PROVIDER)")
    p.add_argument("--model", default=None, help="Model name override")
    p.add_argument("--weak", action="store_true", help="Force weak-device mode")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("models", help="List configured models")

    pi = sub.add_parser("info", help="Show agent + platform info")
    pc = sub.add_parser("chat", help="Send a single chat message")
    pc.add_argument("message", help="Message text")
    pr = sub.add_parser("run", help="Execute a goal (plan -> tools -> verify)")
    pr.add_argument("goal", help="Goal / task description")
    ps = sub.add_parser("server", help="Start the HTTP API server")
    ps.add_argument("--host", default="127.0.0.1")
    ps.add_argument("--port", type=int, default=8000)
    return p


def main(argv=None) -> int:
    configure_logging(level_from_env())
    args = _build_parser().parse_args(argv)

    if args.command in (None,):
        _build_parser().print_help()
        return 0

    if args.command == "server":
        from .api.server import run_server

        run_server(host=args.host, port=args.port, provider=args.provider, model=args.model)
        return 0

    agent = get_agent(provider=args.provider, model=args.model, weak_device=args.weak if args.weak else None)

    if args.command == "models":
        for m in agent.models():
            print(f"- {m['name']} ({m['provider']}): {m['best_for']}")
        return 0

    if args.command == "info":
        print(json.dumps(agent.info(), indent=2))
        return 0

    if args.command == "chat":
        print(agent.chat(args.message))
        return 0

    if args.command == "run":
        result = agent.run(args.goal)
        print(result["summary"])
        v = result["verification"]
        print(f"\n[verification] ok={v.get('ok')} confidence={v.get('confidence')}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())

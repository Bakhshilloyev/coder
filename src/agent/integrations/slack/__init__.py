"""Slack integration (optional; requires `slack_sdk` / `slack-bolt`)."""

from ...runtime.errors import AgentError
from ...runtime.logging import get_logger

logger = get_logger("agent.slack")


def start(token: str = None, provider: str = None) -> None:
    try:
        from slack_bolt import App  # noqa: F401
    except ImportError as exc:
        raise AgentError("slack-bolt is not installed. Run: pip install slack-bolt") from exc
    from ...app import get_agent

    agent = get_agent(provider=provider)
    from slack_bolt import App
    from slack_bolt.adapter.socket_mode import SocketModeHandler

    app = App(token=token or __import__("os").environ.get("SLACK_BOT_TOKEN"))

    @app.message(".*")
    def handle(message, say):
        say(agent.chat(message.get("text", ""))[:3000])

    sk = __import__("os").environ.get("SLACK_APP_TOKEN")
    if not sk:
        raise AgentError("SLACK_APP_TOKEN is not set")
    SocketModeHandler(app, sk).start()

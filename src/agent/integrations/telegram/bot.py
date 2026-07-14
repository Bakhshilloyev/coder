"""Telegram bot integration (optional; requires `python-telegram-bot`)."""

from ...runtime.errors import AgentError
from ...runtime.logging import get_logger

logger = get_logger("agent.telegram")


def _require_sdk():
    try:
        import telegram  # noqa: F401
    except ImportError as exc:
        raise AgentError(
            "python-telegram-bot is not installed. Run: pip install python-telegram-bot"
        ) from exc


def start(token: str = None, provider: str = None) -> None:
    """Start a long-polling Telegram bot bound to the agent.

    Requires TELEGRAM_TOKEN (or pass *token*). Each text message is forwarded
    to :func:`agent.main.chat`.
    """
    _require_sdk()
    import importlib

    from ...app import get_agent

    agent = get_agent(provider=provider)
    from telegram import Update
    from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

    async def on_message(update: "Update", context: "ContextTypes.DEFAULT_TYPE"):
        text = update.message.text
        reply = agent.chat(text)
        await update.message.reply_text(reply[:4000])

    tk = token or __import__("os").environ.get("TELEGRAM_TOKEN")
    if not tk:
        raise AgentError("TELEGRAM_TOKEN is not set")
    app = ApplicationBuilder().token(tk).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    logger.info("telegram bot started")
    app.run_polling()

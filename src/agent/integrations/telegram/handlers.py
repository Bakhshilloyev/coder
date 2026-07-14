"""Telegram command handlers."""

from ...runtime.logging import get_logger

logger = get_logger("agent.telegram.handlers")


def register_handlers(application) -> None:
    """Register /start, /models, /info commands on a Telegram Application."""
    from telegram.ext import CommandHandler

    async def start(update, context):
        await update.message.reply_text("Goat AI Agent online. Send me a task.")

    async def models(update, context):
        from ...app import get_agent

        lines = [f"- {m['name']} ({m['provider']})" for m in get_agent().models()]
        await update.message.reply_text("\n".join(lines) or "(none)")

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("models", models))

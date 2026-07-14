"""Discord integration (optional; requires `discord.py`)."""

from ...runtime.errors import AgentError
from ...runtime.logging import get_logger

logger = get_logger("agent.discord")


def start(token: str = None, provider: str = None) -> None:
    try:
        import discord  # noqa: F401
    except ImportError as exc:
        raise AgentError("discord.py is not installed. Run: pip install discord.py") from exc
    from ...app import get_agent

    agent = get_agent(provider=provider)
    import discord
    from discord.ext import commands

    bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

    @bot.event
    async def on_ready():
        logger.info("discord bot ready: %s", bot.user)

    @bot.command()
    async def ask(ctx, *, message: str):
        await ctx.send(agent.chat(message)[:1900])

    tk = token or __import__("os").environ.get("DISCORD_TOKEN")
    if not tk:
        raise AgentError("DISCORD_TOKEN is not set")
    bot.run(tk)

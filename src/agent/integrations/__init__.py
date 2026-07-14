"""Optional chat-platform integrations (Telegram, Discord, Slack, GitHub).

These modules are import-safe and dependency-free at import time. Each
integration lazily imports its third-party SDK only when started, so the core
agent works everywhere (including Termux / 32-bit) without those packages.
"""

INTEGRATIONS = {
    "telegram": "agent.integrations.telegram",
    "discord": "agent.integrations.discord",
    "slack": "agent.integrations.slack",
    "github": "agent.integrations.github",
}


def available() -> list:
    return list(INTEGRATIONS.keys())

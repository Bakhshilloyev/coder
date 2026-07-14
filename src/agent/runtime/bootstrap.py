"""Bootstrap: assemble a fully configured :class:`Agent` from the environment."""

import os

from ..config import load_config
from ..core.agent import Agent
from ..runtime.logging import configure_logging, level_from_env


def bootstrap(provider: str = None, model: str = None, weak_device: bool = None) -> Agent:
    """Create an :class:`Agent`, configuring logging and provider from env."""
    configure_logging(level_from_env())
    config = load_config()
    agent = Agent(
        config=config,
        provider_name=provider,
        model=model,
        weak_device=weak_device,
    )
    return agent

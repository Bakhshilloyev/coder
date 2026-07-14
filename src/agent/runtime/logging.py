"""Logging setup with a compact, level-aware formatter (stdlib only)."""

import logging
import os
import sys

_CONFIGURED = False


def get_logger(name: str = "agent") -> logging.Logger:
    return logging.getLogger(name)


def configure_logging(level: str | int = "INFO", stream=None) -> None:
    """Configure the root ``agent`` logger once.

    Keeps formatting compact for small terminals (Termux friendly).
    """
    global _CONFIGURED
    if _CONFIGURED:
        if isinstance(level, str):
            logging.getLogger("agent").setLevel(level.upper())
        return

    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    handler = logging.StreamHandler(stream or sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s", "%H:%M:%S"))
    root = logging.getLogger("agent")
    root.setLevel(level)
    root.addHandler(handler)
    root.propagate = False
    _CONFIGURED = True


def level_from_env(default: str = "INFO") -> str:
    return os.environ.get("LOG_LEVEL", default).upper()

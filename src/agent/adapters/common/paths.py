"""Cross-platform path resolution."""

import os
from typing import Optional

from ..common.arch import detect_arch


def data_dir() -> str:
    """Return a writable data directory appropriate for the platform."""
    base = os.environ.get("AGENT_DATA_DIR")
    if base:
        os.makedirs(base, exist_ok=True)
        return base
    home = os.path.expanduser("~")
    if is_termux():
        # Termux: keep inside the app sandbox to avoid permission issues
        d = os.path.join(home, ".termux", "unified-agent", "data")
    else:
        d = os.path.join(home, ".local", "share", "unified-agent")
    os.makedirs(d, exist_ok=True)
    return d


def is_termux() -> bool:
    return os.path.exists("/data/data/com.termux") or "TERMUX_VERSION" in os.environ


def is_windows() -> bool:
    return os.name == "nt"


def is_linux() -> bool:
    return os.name == "posix" and not is_termux()


def runtime_info() -> dict:
    return {
        "os": "windows" if is_windows() else ("termux" if is_termux() else "linux"),
        "arch": detect_arch(),
        "data_dir": data_dir(),
    }

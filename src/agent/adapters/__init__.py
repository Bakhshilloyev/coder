"""Platform adapters: detect OS + architecture and load the right module."""

import platform as _platform

from .common.arch import bits, detect_arch, is_64bit
from .common.env import available_memory_mb, cpu_count, has_command, supports_color
from .common.paths import (
    data_dir,
    is_linux,
    is_termux,
    is_windows,
    runtime_info,
)

__all__ = [
    "bits",
    "detect_arch",
    "is_64bit",
    "available_memory_mb",
    "cpu_count",
    "has_command",
    "supports_color",
    "data_dir",
    "is_linux",
    "is_termux",
    "is_windows",
    "runtime_info",
    "detect_platform",
    "describe",
]


def detect_platform() -> str:
    """Return one of ``linux``, ``windows`` or ``termux``."""
    if is_windows():
        return "windows"
    if is_termux():
        return "termux"
    return "linux"


def describe() -> dict:
    """Return a detailed platform description using the active adapter."""
    name = detect_platform()
    if name == "windows":
        from .windows.platform import describe as _d
    elif name == "termux":
        from .termux.platform import describe as _d
    else:
        from .linux.platform import describe as _d
    info = _d()
    info["python"] = _platform.python_version()
    return info

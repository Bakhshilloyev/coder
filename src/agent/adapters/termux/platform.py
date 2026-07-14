"""Termux (Android) specific platform adapter."""

from ..common.arch import detect_arch
from ..common.env import available_memory_mb, cpu_count, has_command
from ..common.paths import data_dir, runtime_info


def describe() -> dict:
    info = runtime_info()
    info.update(
        {
            "family": "termux",
            "distro": "Android (Termux)",
            "memory_mb": available_memory_mb(),
            "cpus": cpu_count(),
            "has_python": has_command("python"),
            "has_pip": has_command("pip"),
        }
    )
    return info

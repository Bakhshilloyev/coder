"""Windows-specific platform adapter."""

import os
import sys

from ..common.arch import detect_arch
from ..common.env import available_memory_mb, cpu_count
from ..common.paths import data_dir, runtime_info


def describe() -> dict:
    info = runtime_info()
    info.update(
        {
            "family": "windows",
            "distro": f"Windows {sys.getwindowsversion().major}"
            if hasattr(sys, "getwindowsversion")
            else "Windows",
            "memory_mb": available_memory_mb(),
            "cpus": cpu_count(),
        }
    )
    return info

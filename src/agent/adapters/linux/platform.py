"""Linux-specific platform adapter."""

import os

from ..common.arch import detect_arch
from ..common.env import available_memory_mb, cpu_count
from ..common.paths import data_dir, runtime_info


def describe() -> dict:
    info = runtime_info()
    info.update(
        {
            "family": "linux",
            "distro": _distro(),
            "memory_mb": available_memory_mb(),
            "cpus": cpu_count(),
        }
    )
    return info


def _distro() -> str:
    for path in ("/etc/os-release",):
        if os.path.isfile(path):
            try:
                with open(path) as fh:
                    for line in fh:
                        if line.startswith("PRETTY_NAME="):
                            return line.split("=", 1)[1].strip().strip('"')
            except OSError:
                pass
    return "linux"

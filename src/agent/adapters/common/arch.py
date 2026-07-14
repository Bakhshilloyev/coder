"""CPU architecture detection (x86, x64, armv7, arm64, ...)."""

import platform
import re


def detect_arch() -> str:
    """Return a normalised architecture label."""
    raw = platform.machine().lower() or platform.processor().lower()
    if not raw:
        raw = platform.architecture()[0].lower()

    if re.search(r"aarch64|arm64", raw):
        return "arm64"
    if re.search(r"armv7|armv7l|armhf", raw):
        return "armv7"
    if re.search(r"arm", raw):
        return "arm"
    if re.search(r"x86_64|amd64|64", raw):
        return "x64"
    if re.search(r"i[3-6]86|x86|i386", raw):
        return "x86"
    if re.search(r"riscv64", raw):
        return "riscv64"
    if re.search(r"mips", raw):
        return "mips"
    return raw or "unknown"


def is_64bit() -> bool:
    return detect_arch() in ("x64", "arm64", "riscv64")


def bits() -> int:
    return 64 if is_64bit() else 32

"""Environment / capability probing (lightweight, no external deps)."""

import os
import shutil


def has_command(name: str) -> bool:
    return shutil.which(name) is not None


def available_memory_mb() -> int:
    """Best-effort available memory in MB (0 if unknown)."""
    try:
        if os.path.exists("/proc/meminfo"):
            with open("/proc/meminfo") as fh:
                for line in fh:
                    if line.startswith("MemAvailable:"):
                        return int(line.split()[1]) // 1024
        import ctypes

        if hasattr(ctypes, "windll"):
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return int(stat.ullAvailPhys) // (1024 * 1024)
    except Exception:
        return 0
    return 0


def cpu_count() -> int:
    try:
        return os.cpu_count() or 1
    except Exception:
        return 1


def supports_color() -> bool:
    return os.environ.get("NO_COLOR") is None and os.isatty(1)

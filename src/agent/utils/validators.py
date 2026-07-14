"""Lightweight validators for tool arguments and config values."""

from typing import Any


def is_nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_int_str(value: Any) -> bool:
    try:
        int(str(value))
        return True
    except (ValueError, TypeError):
        return False


def choice(value: Any, allowed: list, default: Any = None) -> Any:
    """Return *value* if in *allowed* else *default*."""
    if value in allowed:
        return value
    return default


def required_fields(data: dict, fields: list) -> list:
    """Return the list of missing required field names."""
    return [f for f in fields if f not in data or data[f] in (None, "")]


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))

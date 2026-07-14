"""JSON helpers with safe defaults (stdlib only)."""

import json
from typing import Any, Optional


def load_json(path: str, default: Any = None) -> Any:
    """Load JSON from *path* or return *default* when missing/corrupt."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (FileNotFoundError, ValueError, OSError):
        return default if default is not None else {}


def dump_json(data: Any, path: str, indent: int = 2) -> None:
    """Write *data* as JSON to *path* atomically-ish."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=indent, ensure_ascii=False)
    import os

    os.replace(tmp, path)


def to_json(data: Any, indent: int = 2) -> str:
    return json.dumps(data, indent=indent, ensure_ascii=False)


def from_json(text: str, default: Any = None) -> Any:
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return default if default is not None else {}


def try_parse_json(text: str) -> Optional[Any]:
    """Best-effort JSON parse: strips code fences and trailing prose."""
    text = text.strip()
    if text.startswith("```"):
        # remove ```json / ``` fences
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text)
    except ValueError:
        pass
    # find the first {...} or [...] block
    for opener, closer in (("{", "}"), ("[", "]")):
        start = text.find(opener)
        if start == -1:
            continue
        depth = 0
        for idx in range(start, len(text)):
            if text[idx] == opener:
                depth += 1
            elif text[idx] == closer:
                depth -= 1
                if depth == 0:
                    candidate = text[start : idx + 1]
                    try:
                        return json.loads(candidate)
                    except ValueError:
                        break
    return None

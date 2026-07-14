"""Filesystem helpers used across the agent (stdlib only)."""

import os
from typing import List, Optional


def ensure_dir(path: str) -> str:
    """Create *path* (and parents) if missing and return it."""
    os.makedirs(path, exist_ok=True)
    return path


def list_files(directory: str, recursive: bool = False, ext: Optional[str] = None) -> List[str]:
    """Return a list of file paths under *directory*."""
    results: List[str] = []
    if not os.path.isdir(directory):
        return results
    if recursive:
        for root, _dirs, files in os.walk(directory):
            for name in files:
                if ext and not name.endswith(ext):
                    continue
                results.append(os.path.join(root, name))
    else:
        for name in sorted(os.listdir(directory)):
            full = os.path.join(directory, name)
            if os.path.isfile(full) and (ext is None or name.endswith(ext)):
                results.append(full)
    return results


def safe_join(base: str, *parts: str) -> Optional[str]:
    """Join *parts* onto *base* and refuse to escape *base* (path traversal)."""
    base = os.path.abspath(base)
    target = os.path.abspath(os.path.join(base, *parts))
    if target == base or target.startswith(base + os.sep):
        return target
    return None


def read_text(path: str, encoding: str = "utf-8", limit: Optional[int] = None) -> str:
    with open(path, "r", encoding=encoding, errors="replace") as fh:
        data = fh.read()
    if limit is not None:
        return data[:limit]
    return data


def write_text(path: str, content: str, encoding: str = "utf-8") -> int:
    ensure_dir(os.path.dirname(os.path.abspath(path)))
    with open(path, "w", encoding=encoding) as fh:
        fh.write(content)
    return len(content)

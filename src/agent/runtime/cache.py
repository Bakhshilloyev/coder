"""Tiny TTL cache with an optional on-disk JSON fallback (stdlib only)."""

import json
import os
import threading
import time

from ..utils.json import dump_json, load_json


class Cache:
    """In-memory cache with optional disk persistence and TTL support."""

    def __init__(self, path: str | None = None, ttl: int = 600):
        self._path = path
        self._ttl = ttl
        self._store: dict = {}
        self._lock = threading.Lock()
        if path:
            self._store = load_json(path, {})

    def get(self, key: str):
        with self._lock:
            item = self._store.get(key)
            if not item:
                return None
            if item.get("expires") and item["expires"] < time.time():
                self._store.pop(key, None)
                return None
            return item.get("value")

    def set(self, key: str, value, ttl: int | None = None) -> None:
        ttl = ttl if ttl is not None else self._ttl
        with self._lock:
            self._store[key] = {"value": value, "expires": time.time() + ttl if ttl else 0}
            if self._path:
                dump_json(self._store, self._path)

    def clear(self) -> None:
        with self._lock:
            self._store = {}
            if self._path and os.path.exists(self._path):
                os.remove(self._path)

"""Configuration loader.

Reads the JSON configuration files (``default.json``, ``models.json``,
``permissions.json``, ``routes.json``). The loader searches, in order:

1. the directory pointed to by ``$CONFIG_DIR``
2. ``<project_root>/configs``
3. ``<project_root>`` (legacy / repo root)

This keeps a single source of truth while staying compatible with both the
new ``configs/`` layout and the older repo-root JSON files.
"""

import os
from typing import Any, Dict

from .runtime.errors import ConfigError
from .utils.json import load_json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_CONFIG_FILENAMES = ("default.json", "models.json", "permissions.json", "routes.json")


def _candidate_dirs() -> list:
    dirs = []
    env = os.environ.get("CONFIG_DIR")
    if env:
        dirs.append(env)
    dirs.append(os.path.join(PROJECT_ROOT, "configs"))
    dirs.append(PROJECT_ROOT)
    return dirs


def _find_config(name: str) -> str | None:
    for d in _candidate_dirs():
        candidate = os.path.join(d, name)
        if os.path.isfile(candidate):
            return candidate
    return None


class Config:
    """Holds merged configuration and exposes typed accessors."""

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    @classmethod
    def load(cls) -> "Config":
        data: Dict[str, Any] = {}
        for name in _CONFIG_FILENAMES:
            path = _find_config(name)
            if path:
                loaded = load_json(path, {})
                if isinstance(loaded, dict):
                    data[name.replace(".json", "")] = loaded
        if not data.get("default"):
            raise ConfigError(
                "Could not find default.json in CONFIG_DIR, ./configs or repo root."
            )
        return cls(data)

    # -- generic accessors -------------------------------------------------
    def get(self, key: str, default=None):
        return self._data.get(key, default)

    @property
    def default(self) -> Dict[str, Any]:
        return self._data.get("default", {})

    @property
    def models(self) -> Dict[str, Any]:
        return self._data.get("models", {})

    @property
    def permissions(self) -> Dict[str, Any]:
        return self._data.get("permissions", {})

    @property
    def routes(self) -> Dict[str, Any]:
        return self._data.get("routes", {})

    # -- typed shortcuts ---------------------------------------------------
    @property
    def agent_name(self) -> str:
        return self.default.get("agent_name", "Goat AI Agent")

    @property
    def default_model(self) -> str:
        return self.default.get("default_model", "local")

    @property
    def weak_device_mode(self) -> bool:
        return bool(self.default.get("weak_device_mode", True))

    @property
    def log_level(self) -> str:
        return str(self.default.get("log_level", "INFO")).upper()

    @property
    def memory_db(self) -> str:
        path = self.default.get("memory_db", "data/memory/agent.db")
        if not os.path.isabs(path):
            path = os.path.join(PROJECT_ROOT, path)
        return path


def load_config() -> Config:
    return Config.load()

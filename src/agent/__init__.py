"""Unified Cross-Platform AI Agent.

A lightweight, dependency-free AI agent engine designed to run on Linux,
Windows, and Termux (Android), including 32-bit and weak devices.

The package is organised in layered modules:

- ``core``    : the agent brain (planner, executor, verifier, router, ...)
- ``llm``     : model providers (local, OpenAI, Anthropic, Gemini, Groq, custom)
- ``tools``   : file, shell, web, api, memory and database helpers
- ``adapters``: platform/architecture detection and platform specific behaviour
- ``runtime`` : bootstrap, logging, caching and error handling
- ``memory``  : persistent stores (SQLite) and session management
- ``api``     : a small HTTP server exposing the agent
"""

from .version import __version__

__all__ = ["__version__"]

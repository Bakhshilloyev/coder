"""Policy guard / safety layer.

Screens shell commands and high-risk actions before they run. Dangerous
patterns are blocked outright; mutating commands require confirmation.
"""

import re
from dataclasses import dataclass
from typing import List

# Patterns that must never execute (catastrophic / destructive).
_BLOCKED = [
    r"\brm\s+(-[a-z]*r|-{2}recursive)\s",
    r"\brm\s+-rf\s+/",
    r"\brm\s+-rf\s+~",
    r"\bmkfs\.",
    r"\bdd\s+if=.*of=/dev/",
    r":\(\)\s*\{\s*:\s*\|:&\s*\}",
    r"\bshutdown\b",
    r"\bhalt\b",
    r"\breboot\b",
    r">\s*/dev/sd",
    r"\bchmod\s+-R\s+000\b",
    r"\b(format|clear)\s+disk",
]

# Patterns that need explicit confirmation (not necessarily destructive).
_CONFIRM = [
    r"\bsudo\b",
    r"\brm\b",
    r"\bmv\b",
    r"\bkill\b",
    r"\bgit\s+push\b",
    r"\bgit\s+reset\s+--hard",
    r">",
    r"\bapt\s+(remove|purge)",
]

_BLOCKED_RE = [re.compile(p, re.I) for p in _BLOCKED]
_CONFIRM_RE = [re.compile(p, re.I) for p in _CONFIRM]


@dataclass
class SafetyVerdict:
    allowed: bool
    requires_confirmation: bool = False
    reason: str = ""


def check_command(command: str) -> SafetyVerdict:
    for rx in _BLOCKED_RE:
        if rx.search(command):
            return SafetyVerdict(False, reason=f"matches blocked pattern: {rx.pattern}")
    for rx in _CONFIRM_RE:
        if rx.search(command):
            return SafetyVerdict(True, requires_confirmation=True, reason="mutating command")
    return SafetyVerdict(True)


def is_blocked(text: str) -> bool:
    return any(rx.search(text) for rx in _BLOCKED_RE)


# Simple prompt-injection heuristics for user text.
_INJECTION_HINTS = [
    r"ignore (all|previous|above) instructions",
    r"disregard (your|the) (system|safety) (prompt|rules)",
    r"you are now",
]


def scan_prompt(text: str) -> List[str]:
    hits = []
    for p in _INJECTION_HINTS:
        if re.search(p, text, re.I):
            hits.append(p)
    return hits

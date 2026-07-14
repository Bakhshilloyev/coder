"""Planner: breaks a goal into an ordered list of steps.

Uses the LLM when available; otherwise falls back to a deterministic local
decomposition so planning always works offline.
"""

import json
import re
from typing import Dict, List

from ..llm.provider_base import BaseProvider
from ..runtime.logging import get_logger
from ..utils.json import try_parse_json

logger = get_logger("agent.planner")

_SYSTEM = (
    "You are a task planner for an autonomous agent. Given a goal, return a "
    "JSON object with a 'steps' array. Each step is an object with 'action' "
    "(one of: think, shell, file, web, api, memory) and 'detail' (short "
    "instruction). Only output valid JSON."
)


def plan(goal: str, provider: BaseProvider, weak_device: bool = False) -> Dict:
    if getattr(provider, "name", "") == "local" or weak_device:
        return _local_plan(goal)
    try:
        raw = provider.chat(
            [
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": f"Goal: {goal}"},
            ],
            temperature=0.2,
        )
        parsed = try_parse_json(raw)
        if parsed and isinstance(parsed.get("steps"), list):
            parsed["goal"] = goal
            return parsed
    except Exception as exc:
        logger.warning("LLM planning failed (%s); using local planner", exc)
    return _local_plan(goal)


def _local_plan(goal: str) -> Dict:
    steps: List[Dict] = []
    clauses = re.split(r"\b(then|and|after that|,|;)\b", goal, flags=re.I)
    clauses = [c.strip(" .,;") for c in clauses if c.strip(" .,;") and len(c) > 3]
    if not clauses:
        clauses = [goal]
    for i, clause in enumerate(clauses[:8], 1):
        action = "think"
        if re.search(r"\b(run|execute|install|build|test|command)\b", clause, re.I):
            action = "shell"
        elif re.search(r"\b(fetch|web|search the web|search for|url|http|browse|google|duckduckgo)\b", clause, re.I):
            action = "web"
        elif re.search(r"\b(file|files|read|write|create|edit|list|ls|dir|save)\b", clause, re.I):
            action = "file"
        elif re.search(r"\b(api|call|request)\b", clause, re.I):
            action = "api"
        steps.append({"step": i, "action": action, "detail": clause})
    return {"goal": goal, "steps": steps, "source": "local"}


def summarize_plan(plan: Dict) -> str:
    lines = [f"Plan for: {plan.get('goal', '')}"]
    for s in plan.get("steps", []):
        lines.append(f"  {s.get('step', '?')}. [{s.get('action')}] {s.get('detail')}")
    return "\n".join(lines)

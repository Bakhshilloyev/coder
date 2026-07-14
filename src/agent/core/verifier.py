"""Verifier: checks whether the executed result satisfies the goal."""

from typing import Dict

from ..llm.provider_base import BaseProvider
from ..runtime.logging import get_logger
from ..utils.json import try_parse_json

logger = get_logger("agent.verifier")


def verify(goal: str, result_text: str, provider: BaseProvider) -> Dict:
    if getattr(provider, "name", "") == "local":
        return _local_verify(goal, result_text)
    try:
        raw = provider.chat(
            [
                {
                    "role": "system",
                    "content": "You verify task results. Reply ONLY JSON: "
                    '{"ok": true/false, "confidence": 0-1, "notes": "..."}',
                },
                {
                    "role": "user",
                    "content": f"Goal: {goal}\nResult:\n{result_text[:2000]}",
                },
            ],
            temperature=0.1,
        )
        parsed = try_parse_json(raw)
        if isinstance(parsed, dict) and "ok" in parsed:
            return parsed
    except Exception as exc:
        logger.warning("LLM verification failed (%s); using local verifier", exc)
    return _local_verify(goal, result_text)


def _local_verify(goal: str, result_text: str) -> Dict:
    text = (result_text or "").lower()
    # Word-boundary markers that indicate real failure (avoid matching the
    # result dict's own ``"error":`` key).
    failure_markers = [
        "traceback",
        "exception",
        "permission denied",
        "command not found",
        "no such file",
        "fatal",
        "error:",
        "failed",
        "denied",
        "blocked",
    ]
    ok = bool(result_text) and not any(m in text for m in failure_markers)
    notes = "no errors detected" if ok else "error markers present"
    return {"ok": ok, "confidence": 0.6 if ok else 0.4, "notes": notes}

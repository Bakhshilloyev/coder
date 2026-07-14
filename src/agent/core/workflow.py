"""Workflow orchestration: run a planned sequence of steps.

Implements the Understand -> Plan -> Execute -> Verify -> Improve loop at the
step level. Tool steps are routed/executed; 'think' steps consult the LLM.
"""

from typing import Dict, List

from ..llm.provider_base import BaseProvider
from ..runtime.logging import get_logger
from ..tools import ToolResult
from .executor import Executor
from .planner import summarize_plan
from .verifier import verify

logger = get_logger("agent.workflow")


def execute_plan(
    plan: Dict,
    executor: Executor,
    provider: BaseProvider,
    system: str = "",
) -> List[Dict]:
    logger.info("executing plan:\n%s", summarize_plan(plan))
    results: List[Dict] = []
    context = system
    for step in plan.get("steps", []):
        action = step.get("action", "think")
        detail = step.get("detail", "")
        entry = {"step": step.get("step"), "action": action, "detail": detail}
        if action in ("shell", "file", "web", "api", "memory") and detail:
            res = executor.execute_request(detail)
            if res is None:
                # No tool matched -> treat as a thinking step
                res = _think(detail, provider, context)
            entry["result"] = res.to_dict() if isinstance(res, ToolResult) else str(res)
        else:
            res = _think(detail or plan.get("goal", ""), provider, context)
            entry["result"] = res if isinstance(res, str) else res.to_dict()
        results.append(entry)
    return results


def _think(detail: str, provider: BaseProvider, context: str) -> ToolResult:
    prompt = f"{context}\n\nTask: {detail}\n\nProvide a concise response."
    try:
        out = provider.complete(prompt)
        return ToolResult(True, out)
    except Exception as exc:
        return ToolResult(False, "", error=str(exc))


def improve(goal: str, results: List[Dict], provider: BaseProvider) -> Dict:
    combined = "\n".join(
        f"Step {r.get('step')}: {r.get('detail')}\n-> {r.get('result')}" for r in results
    )
    return verify(goal, combined, provider)

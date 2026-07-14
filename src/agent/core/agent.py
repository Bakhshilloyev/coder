"""Central agent: ties together provider, memory, router, planner, executor."""

from typing import Callable, Dict, List, Optional

from ..config import Config, load_config
from ..llm.model_registry import build_provider, list_models
from ..runtime.logging import get_logger
from ..tools.memory_tools import init_memory
from .memory import Memory
from .planner import plan, summarize_plan
from .executor import Executor
from .tool_router import ToolRouter
from .verifier import verify
from .workflow import execute_plan, improve

logger = get_logger("agent.core")


class Agent:
    def __init__(
        self,
        config: Optional[Config] = None,
        provider_name: Optional[str] = None,
        model: Optional[str] = None,
        confirm: Optional[Callable[[str], bool]] = None,
        weak_device: Optional[bool] = None,
    ):
        self.config = config or load_config()
        self.weak_device = (
            weak_device if weak_device is not None else self.config.weak_device_mode
        )
        self.provider = build_provider(provider_name, model)
        self.memory = Memory(self.config.memory_db)
        init_memory(self.memory.store)
        self.router = ToolRouter()
        self.executor = Executor(self.router, confirm=confirm)
        self.system_prompt = (
            f"You are {self.config.agent_name}, a helpful cross-platform AI agent. "
            "You can use file, shell, web, api and memory tools. Be concise and safe."
        )
        logger.info(
            "agent ready: provider=%s weak_device=%s", self.provider.name, self.weak_device
        )

    # -- conversational --------------------------------------------------
    def chat(self, message: str) -> str:
        self.memory.add_turn("user", message)
        routed = self.executor.execute_request(message)
        if routed is not None:
            answer = routed.output or routed.error or "(no output)"
            self.memory.add_turn("assistant", answer)
            return answer
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.memory.context_messages())
        out = self.provider.chat(messages)
        self.memory.add_turn("assistant", out)
        return out

    # -- goal-driven workflow -------------------------------------------
    def run(self, goal: str) -> Dict:
        self.memory.add_turn("user", goal)
        p = plan(goal, self.provider, weak_device=self.weak_device)
        results = execute_plan(
            p, self.executor, self.provider, system=self.system_prompt
        )
        verdict = improve(goal, results, self.provider)
        summary = "\n".join(
            f"{r.get('step')}. [{r.get('action')}] {r.get('detail')}\n   {_short(r.get('result'))}"
            for r in results
        )
        final = {
            "goal": goal,
            "plan": p,
            "steps": results,
            "verification": verdict,
            "provider": self.provider.name,
            "summary": summary,
        }
        self.memory.add_turn("assistant", summary)
        return final

    # -- introspection ---------------------------------------------------
    def models(self) -> List[Dict]:
        return list_models(self.config)

    def info(self) -> Dict:
        from ..adapters import describe

        return {
            "name": self.config.agent_name,
            "version": __import__("agent").__version__,
            "provider": self.provider.name,
            "weak_device": self.weak_device,
            "platform": describe(),
            "tools": [t["name"] for t in self.router.list_tools()],
        }


def _short(result) -> str:
    if isinstance(result, dict):
        return str(result.get("output", ""))[:300]
    return str(result)[:300]

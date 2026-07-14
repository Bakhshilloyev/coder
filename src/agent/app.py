"""Application factory + shared singletons (lazy)."""

from .core.agent import Agent
from .runtime.bootstrap import bootstrap
from .runtime.dispatcher import Dispatcher

_agent: Agent | None = None
_dispatcher: Dispatcher | None = None


def get_agent(provider: str = None, model: str = None, weak_device: bool = None) -> Agent:
    global _agent
    if _agent is None:
        _agent = bootstrap(provider, model, weak_device)
    return _agent


def get_dispatcher() -> Dispatcher:
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = Dispatcher(get_agent())
    return _dispatcher

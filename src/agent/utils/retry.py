"""Retry helper with exponential backoff (stdlib only)."""

import time
from typing import Callable, Type, Tuple


def retry(
    func: Callable,
    *args,
    attempts: int = 3,
    backoff: float = 0.5,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    on_retry: Callable[[int, Exception], None] | None = None,
    **kwargs,
):
    """Call *func* up to *attempts* times with exponential backoff."""
    delay = backoff
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return func(*args, **kwargs)
        except exceptions as exc:  # type: ignore[misc]
            last_exc = exc
            if on_retry:
                on_retry(attempt, exc)
            if attempt >= attempts:
                break
            time.sleep(delay)
            delay *= backoff_factor
    assert last_exc is not None
    raise last_exc

# app/core/decorators/log_decorators.py

import logging
from collections.abc import Callable
from functools import wraps

logger = logging.getLogger(__name__)


def log_execution[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator for logging function execution lifecycle.

    Logs:
    - START before function execution
    - END after successful execution
    - DEBUG diagnostics if an exception occurs

    Args:
        func (Callable): Function to wrap.

    Returns:
        Callable: Wrapped function.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        func_name = func.__name__

        logger.debug(f"[cyan]▶ COMMAND START[/cyan] | [dim]{func_name}[/dim]")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"[green]✔ COMMAND END[/green] | [dim]{func_name}[/dim]")
            return result
        except Exception as exc:
            logger.debug(
                "Command '%s' failed: %s",
                func_name,
                exc,
                exc_info=True,
            )
            raise

    return wrapper

# app/cli/errors.py

"""Reusable exception boundaries for user-facing Reflow commands."""

from __future__ import annotations

import logging
from collections.abc import Callable
from functools import wraps

import typer
from click.exceptions import Abort, ClickException, Exit

from app.core.shared import ReflowError
from app.ui.exceptions import show_error

logger = logging.getLogger(__name__)


def handle_cli_errors[**P, R](
    operation: str,
    *,
    solution: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Convert application failures into concise CLI errors.

    Args:
        operation:
            User-facing workflow name included in the error panel.

        solution:
            Optional actionable guidance for expected Reflow failures.

    Returns:
        Callable:
            Decorator preserving the wrapped Typer command signature.

    Notes:
        Click control-flow exceptions remain unchanged. Expected domain errors
        include their safe message, while unexpected exceptions hide internal
        details from normal console output. Complete tracebacks remain
        available through debug logging.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except Exit, Abort, ClickException, typer.Exit, typer.Abort:
                raise
            except ReflowError as exc:
                logger.debug(
                    "%s failed: %s",
                    operation,
                    exc,
                    exc_info=True,
                )
                message = f"{operation} failed\n\n{exc}"
                if solution:
                    message += f"\n\nSolution\n\n{solution}"
                show_error(message)
                raise typer.Exit(code=1) from None
            except Exception as exc:
                logger.debug(
                    "%s failed unexpectedly: %s",
                    operation,
                    exc,
                    exc_info=True,
                )
                show_error(
                    f"{operation} failed unexpectedly.\n\n"
                    "Re-run with --debug and inspect the configured log file "
                    "for technical details."
                )
                raise typer.Exit(code=1) from None

        return wrapper

    return decorator

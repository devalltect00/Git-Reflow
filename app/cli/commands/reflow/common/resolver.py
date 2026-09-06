# app/cli/commands/reflow/common/resolver.py

"""
Resolver utilities shared by Reflow commands.

This module converts:

    global execution context
        +
    command specific values
        +
    configuration values

into strongly typed argument models.
"""

from app.cli.commands.reflow.common.models import ReflowExecutionArgs
from app.core.repository import RepositoryTarget


def resolve_execution_args(
    *,
    dry_run: bool,
    debug: bool,
    log_level,
    repository: RepositoryTarget,
    progress_enabled: bool,
) -> ReflowExecutionArgs:
    """
    Resolve shared execution arguments.

    Parameters
    ----------
    dry_run:
        Dry-run execution mode.

    debug:
        Debug mode flag.

    log_level:
        Effective logging level.

    repository:
        Validated local or remote repository target.

    progress_enabled:
        Display progress indicators for long-running command work.

    Returns
    -------
    ReflowExecutionArgs
    """

    return ReflowExecutionArgs(
        dry_run=dry_run,
        debug=debug,
        log_level=log_level,
        silent=False,
        repository=repository,
        progress_enabled=progress_enabled,
    )

# app/cli/commands/reflow/tags/replay/models.py

"""
Argument models for:

    reflow tags replay

These models represent fully-resolved and validated
arguments ready for backend execution.
"""

from dataclasses import dataclass

from app.cli.commands.reflow.common.models import (
    ReflowExecutionArgs,
)


@dataclass(slots=True)
class ReplayTagsArgs(ReflowExecutionArgs):
    """
    Replay tags command arguments.

    All values have already been resolved from:

        CLI
            ↓
        Config
            ↓
        Defaults
    """

    delay: int
    only_stable: bool
    limit: int | None

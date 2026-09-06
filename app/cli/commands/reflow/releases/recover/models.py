# app/cli/commands/reflow/releases/recover/models.py

"""Resolved argument model for ``reflow releases recover``."""

from dataclasses import dataclass

from app.cli.commands.reflow.common.models import ReflowExecutionArgs


@dataclass(slots=True)
class RecoverReleasesArgs(ReflowExecutionArgs):
    """Validated release-recovery arguments."""

    delay: int
    only_stable: bool
    limit: int | None
    yes: bool

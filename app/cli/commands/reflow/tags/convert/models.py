# app/cli/commands/reflow/tags/convert/models.py

"""
Argument models for:

    reflow tags convert local|remote

These models represent fully-resolved and validated
arguments ready for backend execution.
"""

from dataclasses import dataclass
from enum import StrEnum

from app.cli.commands.reflow.common.models import (
    ReflowExecutionArgs,
)
from app.core.reflow import TagFormat


class TagConversionScope(StrEnum):
    """Persistent destination selected by a tag-conversion subcommand."""

    LOCAL = "local"
    REMOTE = "remote"


@dataclass(slots=True)
class ConvertTagsArgs(ReflowExecutionArgs):
    """
    Convert tags command arguments.

    Attributes:
        scope:
            Replace local or remote tag references.

        target_format:
            Destination version-tag format.

        yes:
            Skip the live-operation confirmation prompt.
    """

    scope: TagConversionScope = TagConversionScope.LOCAL
    target_format: TagFormat = TagFormat.SEMVER
    yes: bool = False

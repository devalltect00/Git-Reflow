# app/cli/commands/reflow/common/models.py

"""
Shared models used by Reflow commands.

Commands
--------
reflow releases recover
reflow tags convert local|remote
reflow dockerize

This module contains shared argument models that represent
fully-resolved and validated execution values.

These models are independent from:

    - Typer
    - TOML configuration
    - backend implementation

The resolver layer is responsible for converting
raw CLI/config values into these models.
"""

from dataclasses import dataclass

from app.cli.constants.enums import LogLevelChoices
from app.core.repository import RepositoryTarget


@dataclass(slots=True)
class ReflowExecutionArgs:
    """
    Shared execution arguments.

    These values originate from the global CLI layer
    and are inherited by all Reflow commands.

    Attributes
    ----------
    dry_run:
        Simulate execution without making changes.

    debug:
        Enable verbose debugging output.

    log_level:
        Effective logging level.

    silent:
            Suppress command execution output.
    """

    dry_run: bool
    debug: bool
    log_level: LogLevelChoices
    silent: bool
    repository: RepositoryTarget
    progress_enabled: bool

    def model_dump(self) -> dict:
        """
        Convert execution arguments to dictionary.

        Useful when extending ReflowExecutionArgs
        in command-specific argument models.

        Returns
        -------
        dict
        """

        return {
            "dry_run": self.dry_run,
            "debug": self.debug,
            "log_level": self.log_level,
            "silent": self.silent,
            "repository": self.repository,
            "progress_enabled": self.progress_enabled,
        }

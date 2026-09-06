# app/core/dry_run/dry_run_support.py

"""
Dry-run support utilities.

This module provides a reusable base class that exposes
a configured Runner instance.

Classes that need command execution can inherit from
DryRunSupport instead of creating Runner manually.
"""

from .dry_run import Runner


class DryRunSupport:
    """
    Shared dry-run support.

    Provides a reusable Runner instance for classes that
    need command execution with dry-run and silent mode
    support.
    """

    def __init__(
        self,
        dry_run: bool = False,
        is_silent: bool = False,
    ) -> None:
        """
        Initialize dry-run support.

        Args:
            dry_run:
                Enable dry-run mode.

            is_silent:
                Suppress command logging.
        """
        self.runner = Runner(
            is_dry_run=dry_run,
            is_silent=is_silent,
        )

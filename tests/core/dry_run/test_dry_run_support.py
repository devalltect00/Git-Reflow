# tests/core/dry_run/test_dry_run_support.py

"""
Tests for DryRunSupport.
"""

from app.core.dry_run.dry_run import Runner
from app.core.dry_run.dry_run_support import (
    DryRunSupport,
)


class TestDryRunSupport:
    """
    Tests for DryRunSupport.
    """

    def test_creates_runner(self):
        """
        Should create Runner instance.
        """
        support = DryRunSupport()

        assert isinstance(
            support.runner,
            Runner,
        )

    def test_passes_dry_run_to_runner(self):
        """
        Should pass dry-run option.
        """
        support = DryRunSupport(
            dry_run=True,
        )

        assert support.runner.get_is_dry_run() is True

    def test_passes_silent_to_runner(self):
        """
        Should pass silent option.
        """
        support = DryRunSupport(
            is_silent=True,
        )

        assert support.runner.get_silent() is True

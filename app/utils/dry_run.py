# app\utils\dry_run.py

import logging
import subprocess
from collections.abc import Callable

logger = logging.getLogger(__name__)


class Runner:
    """
    Executes shell commands with optional dry-run support.
    """

    def __init__(self, is_dry_run: bool = False):
        self.is_dry_run = is_dry_run

    def run(
        self,
        command: list[str],
        on_error: Callable | None = None,
        **kwargs,
    ) -> subprocess.CompletedProcess | None:
        """
        Execute a command safely.

        Args:
            command (list[str]): Command to run
            on_error (Callable): Optional error handler

        Returns:
            CompletedProcess or None
        """
        if not self.is_dry_run:
            logger.info(f"→ {' '.join(command)}")
            try:
                return subprocess.run(command, **kwargs)
            except subprocess.CalledProcessError:
                if on_error:
                    on_error()
                return None
        else:
            logger.info(f"(dry-run) ✅ {' '.join(command)}")
            return None
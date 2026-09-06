# app/core/dry_run/dry_run.py

"""
Command execution utilities.

This module provides a reusable command runner with support
for:

- Dry-run mode
- Silent mode
- Logging
- Error callbacks

The Runner class is shared by Git, GitHub, Docker, and
future command executors.
"""

import logging
import subprocess
from collections.abc import Callable

logger = logging.getLogger(__name__)


def format_command(
    command: str | list[str],
) -> str:
    """
    Convert a command into a shell-like string.

    Args:
        command:
            Command string or list of command parts.

    Returns:
        Formatted command string.
    """
    if isinstance(command, list):
        return " ".join(command)

    return command


def log_command(
    command: str,
) -> None:
    """
    Log a command.

    Args:
        command:
            Command to log.
    """
    logger.debug(
        "[primary]cmd[/primary]: [text]%s[/text]",
        command,
    )


def log_command_with_pointing(
    command: str,
) -> None:
    """
    Log a command with a pointing indicator.

    Args:
        command:
            Command to log.
    """
    logger.debug(
        "[pointing]→[/pointing] [text]%s[/text]",
        command,
    )


def log_dry_run(
    command: str,
) -> None:
    """
    Log a simulated command execution.

    Args:
        command:
            Command being simulated.
    """
    logger.info(
        "[dry_run](dry-run)[/dry_run] [success]✔[/success] Simulated: [text]%s[/text]",
        command,
    )


class Runner:
    """
    Execute shell commands.

    Supports:

    - Dry-run mode
    - Silent mode
    - Error callbacks
    - Additional subprocess arguments
    """

    def __init__(
        self,
        is_dry_run: bool = False,
        is_silent: bool = False,
    ) -> None:
        """
        Initialize runner.

        Args:
            is_dry_run:
                Enable dry-run mode.

            is_silent:
                Suppress command logging.
        """
        self.is_dry_run = is_dry_run
        self.silent = is_silent

    def set_is_dry_run(
        self,
        is_dry_run: bool,
    ) -> None:
        """
        Set dry-run mode.

        Args:
            is_dry_run:
                New dry-run state.
        """
        self.is_dry_run = is_dry_run

    def get_is_dry_run(
        self,
    ) -> bool:
        """
        Get dry-run state.

        Returns:
            Current dry-run state.
        """
        return self.is_dry_run

    def set_silent(
        self,
        is_silent: bool,
    ) -> None:
        """
        Set silent mode.

        Args:
            is_silent:
                New silent state.
        """
        self.silent = is_silent

    def get_silent(
        self,
    ) -> bool:
        """
        Get silent mode state.

        Returns:
            Current silent state.
        """
        return self.silent

    def run(
        self,
        command: str | list[str],
        on_error: Callable[[], None] | None = None,
        *,
        mutates: bool = True,
        **kwargs,
    ) -> subprocess.CompletedProcess | None:
        """
        Execute a command.
        Run a shell command and handle any error with a custom function.

        Args:
            command:
                Command to execute.

            on_error:
                Optional callback executed when the
                command fails.

            mutates:
                Whether the command changes external or local state. Read-only
                commands continue to run in dry-run mode so workflows can
                discover and display their planned targets.

            **kwargs:
                Additional arguments passed to
                subprocess.run().

        Returns:
            CompletedProcess after execution, including normalized command
            failures. Returns ``None`` only when a mutating command is skipped
            by dry-run mode.
        """
        if "shell" not in kwargs:
            kwargs["shell"] = False

        if not self.is_dry_run or not mutates:
            if not self.get_silent():
                log_command_with_pointing(
                    format_command(command),
                )

            try:
                # Avoid `shell=False` when passing **untrusted input**, to prevent shell injection attacks.
                result = subprocess.run(
                    command,
                    **kwargs,
                )
                return result
            except subprocess.CalledProcessError as exc:
                if on_error:
                    on_error()

                return subprocess.CompletedProcess(
                    args=exc.cmd,
                    returncode=exc.returncode,
                    stdout=exc.stdout,
                    stderr=exc.stderr,
                )

        log_dry_run(
            format_command(command),
        )

        return None

    def check_output(
        self,
        command: str | list[str],
        on_error: Callable[[], None] | None = None,
        *,
        mutates: bool = True,
        **kwargs,
    ) -> str | bytes | None:
        """
        Execute a command and return its output.

        Args:
            command:
                Command to execute.

            on_error:
                Optional callback executed when the
                command fails.

            **kwargs:
                Additional arguments passed to
                subprocess.check_output().

        Returns:
            Command output, or None if execution fails
            or dry-run mode is enabled.
        """
        # If user did not pass `shell`, ue default
        if "shell" not in kwargs:
            kwargs["shell"] = False  # safest default

        if not self.is_dry_run or not mutates:
            if not self.get_silent():
                log_command_with_pointing(
                    format_command(command),
                )

            try:
                # Avoid `shell=False` when passing **untrusted input**, to prevent shell injection attacks.
                output = subprocess.check_output(
                    command,
                    **kwargs,
                )

                return (
                    output.decode()
                    if isinstance(output, bytes) and kwargs.get("text", True)
                    else output
                )

            except subprocess.CalledProcessError:
                if on_error:
                    on_error()

                return None

        log_dry_run(
            format_command(command),
        )

        return None

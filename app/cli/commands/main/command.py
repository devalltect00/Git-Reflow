# app/cli/commands/main/command.py

import logging
import sys

import typer

from app.cli.commands.main.options import (
    DebugOption,
    DryRunOption,
    HelpOption,
    LogLevelOption,
    NoBannerOption,
    RepositoryOption,
    RepositoryUrlOption,
    VersionOption,
)
from app.cli.commands.main.resolver import resolve_main_args
from app.cli.commands.reflow.common.models import ReflowExecutionArgs
from app.cli.commands.reflow.common.resolver import resolve_execution_args
from app.cli.constants.args import CliArgs
from app.config.config_loader import get_config
from app.core.shared import ConfigurationError
from app.ui.banner import banner
from app.ui.exceptions import show_error
from app.utils.logging import setup_logging


class _ExecutionContext:
    """Resolve operational configuration only when a command needs it.

    Typer invokes the root callback before rendering nested command help. A
    lazy context therefore keeps informational help available even when the
    configured repository target is invalid, while executed commands still
    receive the same validation and actionable error reporting.
    """

    def __init__(self, cli_args: CliArgs) -> None:
        self._cli_args = cli_args
        self._execution_args: ReflowExecutionArgs | None = None

    @property
    def execution_args(self) -> ReflowExecutionArgs:
        """Return resolved execution arguments, caching the first result."""

        if self._execution_args is None:
            try:
                config = get_config()
                args = resolve_main_args(config=config, cli_args=self._cli_args)
            except ConfigurationError as exc:
                logging.getLogger("main").debug(
                    "Failed to resolve Reflow configuration: %s",
                    exc,
                )
                show_error(_configuration_error_message(exc, self._cli_args))
                raise typer.Exit(code=2) from None

            self._execution_args = resolve_execution_args(
                dry_run=args.dry_run,
                debug=args.debug,
                log_level=args.log_level,
                repository=args.repository,
                progress_enabled=args.progress_enabled,
            )
            setup_logging(level=args.log_level, debug=args.debug)

        return self._execution_args


def _configuration_error_message(
    error: ConfigurationError,
    cli_args: CliArgs,
) -> str:
    """Build actionable guidance for a root configuration failure.

    Args:
        error:
            Validation error raised while resolving global settings.

        cli_args:
            Explicit command-line values used to identify the conflicting
            target-selection source.

    Returns:
        str:
            User-facing error text with a concrete correction.
    """

    if cli_args.repository is not None and cli_args.repository_url is not None:
        solution = (
            "Pass exactly one repository target option:\n\n"
            "Local checkout:\n"
            "  reflow --repository PATH <command>\n\n"
            "Remote URL:\n"
            "  reflow --repository-url URL <command>"
        )
    else:
        solution = (
            "In .config/reflow/config.toml, keep exactly one target active:\n\n"
            "Local checkout:\n"
            '  path = "D:/path/to/repository"\n'
            '  # url = "https://github.com/owner/project.git"\n\n'
            "Remote URL:\n"
            '  # path = "D:/path/to/repository"\n'
            '  url = "https://github.com/owner/project.git"'
        )

    return f"Configuration error\n\n{error}\n\nSolution\n\n{solution}"


def main(
    ctx: typer.Context,
    no_banner: NoBannerOption = None,
    help: HelpOption = None,
    version: VersionOption = None,
    dry_run: DryRunOption = None,
    debug: DebugOption = None,
    log_level: LogLevelOption = None,
    repository: RepositoryOption = None,
    repository_url: RepositoryUrlOption = None,
) -> None:
    """Resolve global state and initialize the shared command context."""

    # Root help is informational and must remain available even when an
    # operational repository target is unavailable in the current runtime.
    if help:
        if not no_banner:
            banner.show()
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)

    # REQUIRED defaults
    cli_args = CliArgs(
        no_banner=no_banner,
        help=help,
        version=version,
        dry_run=dry_run,
        debug=debug,
        log_level=log_level,
        repository=repository,
        repository_url=repository_url,
    )

    # =========================================================
    # SHARED REFLOW EXECUTION CONTEXT
    # =========================================================

    ctx.obj = _ExecutionContext(cli_args)

    if not no_banner:
        banner.show()

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)

    full_command = " ".join(sys.argv[1:])
    logger = logging.getLogger("main")
    logger.debug("[cyan]CLI COMMAND[/cyan] | [dim]Reflow %s[/dim]", full_command)

# app/cli/commands/main/resolver.py

from app.cli.constants.enums import LogLevelChoices
from app.core.repository import RepositoryTarget

from .models import MainArgs


def resolve_repository_target(config, cli_args) -> RepositoryTarget:
    """
    Resolve the repository target from CLI, configuration, and defaults.

    An explicit CLI path or URL replaces configured target values. Path and
    URL forms at the same priority level are mutually exclusive.

    Args:
        config:
            Reflow configuration loader.

        cli_args:
            Raw global CLI arguments.

    Returns:
        RepositoryTarget:
            Validated local or remote repository target.
    """

    if cli_args.repository is not None or cli_args.repository_url is not None:
        return RepositoryTarget.resolve(
            cli_args.repository,
            url=cli_args.repository_url,
        )

    return RepositoryTarget.resolve(
        config.get("repository", "path", default=None),
        url=config.get("repository", "url", default=None),
    )


def resolve_main_args(config, cli_args) -> MainArgs:
    """Resolve global CLI arguments into an execution-ready model."""

    return MainArgs(
        no_banner=cli_args.no_banner or False,
        help=cli_args.help or False,
        version=cli_args.version or None,
        dry_run=config.resolve(
            cli_args.dry_run,
            ["cli", "execution", "dry_run"],
            False,
        ),
        debug=config.resolve(
            cli_args.debug,
            ["cli", "execution", "debug"],
            False,
        ),
        log_level=config.resolve(
            cli_args.log_level,
            ["logging", "level"],
            LogLevelChoices.INFO,
        ),
        repository=resolve_repository_target(config, cli_args),
        progress_enabled=config.resolve(
            None,
            ["cli", "progress", "enabled"],
            True,
        ),
    )

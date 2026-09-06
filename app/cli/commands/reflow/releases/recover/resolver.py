# app/cli/commands/reflow/releases/recover/resolver.py

"""Resolve CLI and configuration values for release recovery."""

from app.cli.commands.reflow.releases.recover.models import RecoverReleasesArgs
from app.config.config_loader import get_config


def resolve_recover_releases_args(
    *,
    execution_args,
    delay,
    only_stable,
    limit,
    yes: bool,
) -> RecoverReleasesArgs:
    """
    Resolve release-recovery arguments.

    The former ``cli.tags.replay`` values remain fallbacks during the command
    migration so existing configuration files keep working.
    """

    config = get_config()
    legacy_delay = config.get("cli", "tags", "replay", "delay", default=2)
    legacy_stable = config.get("cli", "tags", "replay", "only_stable", default=False)
    legacy_limit = config.get("cli", "tags", "replay", "limit", default=None)

    return RecoverReleasesArgs(
        **execution_args.model_dump(),
        delay=config.resolve(
            delay,
            ["cli", "releases", "recover", "delay"],
            legacy_delay,
        ),
        only_stable=config.resolve(
            only_stable,
            ["cli", "releases", "recover", "only_stable"],
            legacy_stable,
        ),
        limit=config.resolve(
            limit,
            ["cli", "releases", "recover", "limit"],
            legacy_limit,
        ),
        yes=yes,
    )

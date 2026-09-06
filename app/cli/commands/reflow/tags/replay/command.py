# app/cli/commands/reflow/tags/replay/command.py

"""
Deprecated release-recovery compatibility alias.

Command:

    reflow tags replay

Delegates old ``reflow tags replay`` invocations to the canonical
``reflow releases recover`` workflow.
"""

import typer

from app.cli.commands.reflow.releases.recover.command import run_recover_releases
from app.cli.commands.reflow.releases.recover.options import YesOption
from app.cli.commands.reflow.tags.replay.options import (
    DelayOption,
    LimitOption,
    OnlyStableOption,
)
from app.cli.errors import handle_cli_errors
from app.cli.help import REPLAY_HELP
from app.ui.console import console
from app.ui.panels import warning_panel

app = typer.Typer(
    invoke_without_command=True,
    help="""
    DEPRECATED compatibility alias for `reflow releases recover`.

    Existing scripts continue to work, but new usage should call
    `reflow releases recover`.
    """,
)


@app.callback(help=REPLAY_HELP)
@handle_cli_errors(
    "Release recovery",
    solution=(
        "Use the canonical 'reflow releases recover' command, verify GitHub CLI "
        "authentication and the configured remote, then preview with --dry-run."
    ),
)
def replay(
    ctx: typer.Context,
    delay: DelayOption = None,
    only_stable: OnlyStableOption = None,
    limit: LimitOption = None,
    yes: YesOption = False,
):
    """Warn about deprecation and run canonical release recovery."""

    console.print(
        warning_panel(
            "DEPRECATED COMMAND: 'reflow tags replay' is retained only as a "
            "compatibility alias. Use 'reflow releases recover' instead."
        )
    )
    run_recover_releases(
        ctx,
        delay=delay,
        only_stable=only_stable,
        limit=limit,
        yes=yes,
    )

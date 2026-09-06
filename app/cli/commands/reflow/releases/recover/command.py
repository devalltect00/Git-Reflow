# app/cli/commands/reflow/releases/recover/command.py

"""Recover missing GitHub releases by re-pushing their existing tags."""

import typer

from app.cli.commands.reflow.releases.recover.options import (
    DelayOption,
    LimitOption,
    OnlyStableOption,
    YesOption,
)
from app.cli.commands.reflow.releases.recover.resolver import (
    resolve_recover_releases_args,
)
from app.cli.errors import handle_cli_errors
from app.cli.help import RECOVER_RELEASES_HELP
from app.core.reflow import ReleaseRecovery
from app.core.repository import RepositoryWorkspace
from app.ui.console import console
from app.ui.panels import summary_panel, warning_panel

app = typer.Typer(
    invoke_without_command=True,
    help="Recover missing releases by re-pushing existing version tags.",
)


def run_recover_releases(
    ctx: typer.Context,
    *,
    delay: int | None = None,
    only_stable: bool | None = None,
    limit: int | None = None,
    yes: bool = False,
) -> None:
    """
    Execute the release-recovery workflow.

    Args:
        ctx:
            Typer context containing shared execution arguments.

        delay:
            Delay between remote tag operations.

        only_stable:
            Select stable version tags only.

        limit:
            Maximum number of tags to process.

        yes:
            Skip the live-operation confirmation prompt.
    """

    args = resolve_recover_releases_args(
        execution_args=ctx.obj.execution_args,
        delay=delay,
        only_stable=only_stable,
        limit=limit,
        yes=yes,
    )

    operation = (
        "Preview    : would delete and re-push remote tags with missing releases\n"
        "Changes    : none (dry-run)"
        if args.dry_run
        else "Operation  : delete and re-push remote tags with missing releases"
    )

    console.print(
        summary_panel(
            title="Release Recovery Target",
            message=f"Repository : {args.repository.display}\n{operation}",
        )
    )

    if not args.dry_run and not args.yes:
        console.print(
            warning_panel("This operation deletes and re-pushes selected remote tags.")
        )
        typer.confirm("Continue with release recovery?", abort=True)

    workspace = RepositoryWorkspace(
        args.repository,
        dry_run=args.dry_run,
        is_silent=args.silent,
        progress_enabled=args.progress_enabled,
    )
    with workspace.materialize() as repository:
        recovery = ReleaseRecovery(
            dry_run=args.dry_run,
            is_silent=args.silent,
            delay=args.delay,
            repository=repository,
            progress_enabled=args.progress_enabled,
        )
        succeeded = recovery.run(
            only_stable=args.only_stable,
            limit=args.limit,
        )
        if succeeded is False:
            raise typer.Exit(code=1)


@app.callback(help=RECOVER_RELEASES_HELP)
@handle_cli_errors(
    "Release recovery",
    solution=(
        "Verify Git and GitHub CLI authentication, the configured remote, and "
        "the repository's tag-based release workflow. Preview with --dry-run."
    ),
)
def recover_releases(
    ctx: typer.Context,
    delay: DelayOption = None,
    only_stable: OnlyStableOption = None,
    limit: LimitOption = None,
    yes: YesOption = False,
) -> None:
    """Recover missing releases for the selected repository."""

    run_recover_releases(
        ctx,
        delay=delay,
        only_stable=only_stable,
        limit=limit,
        yes=yes,
    )

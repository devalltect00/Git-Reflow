# app/cli/commands/reflow/tags/convert/command.py

"""Preview, confirm, and atomically replace converted Git tag names."""

from __future__ import annotations

import logging
from pathlib import Path

import typer
from rich.table import Table

from app.cli.commands.reflow.tags.convert.models import (
    ConvertTagsArgs,
    TagConversionScope,
)
from app.cli.commands.reflow.tags.convert.resolver import resolve_convert_tags_args
from app.cli.errors import handle_cli_errors
from app.cli.help.reflow.tags.convert.help import CONVERT_HELP
from app.core.git import GitService, create_git_service
from app.core.reflow import (
    TagConversionPlan,
    TagConverter,
    TagFormat,
    TagReplacementService,
)
from app.core.repository import RepositoryWorkspace
from app.core.shared import ReflowError
from app.ui.console import console
from app.ui.panels import error_panel, success_panel, summary_panel, warning_panel
from app.ui.progress import progress_spinner, progress_task

from .options import TargetFormatOption, YesOption

logger = logging.getLogger(__name__)

app = typer.Typer(
    no_args_is_help=True,
    help=CONVERT_HELP,
)


def _validate_repository(git: GitService) -> None:
    """Reject a materialized target that is not a Git repository."""

    if git.is_git_repo():
        return
    console.print(error_panel("❌ Target directory is not a Git repository."))
    raise typer.Exit(code=1)


def _conversion_table(plan: TagConversionPlan) -> Table:
    """Create a source-to-destination replacement preview."""

    table = Table(title="Planned Tag Replacements", show_lines=True)
    table.add_column("Source tag", style="yellow")
    table.add_column("Destination tag", style="green")
    for item in plan.conversions:
        table.add_row(item.source, item.destination)
    return table


def _skipped_table(plan: TagConversionPlan) -> Table:
    """Create a table explaining excluded tags."""

    table = Table(title="Skipped Tags", show_lines=True)
    table.add_column("Tag", style="yellow")
    table.add_column("Reason")
    for item in plan.skipped:
        table.add_row(item.tag, item.reason)
    return table


def _show_plan(*, args: ConvertTagsArgs, plan: TagConversionPlan) -> None:
    """Display the explicit persistence scope and complete replacement plan."""

    mode = "dry-run (no changes)" if args.dry_run else "live"
    scope_description = (
        "local ref transaction"
        if args.scope is TagConversionScope.LOCAL
        else "guarded atomic remote push"
    )
    console.print(
        summary_panel(
            title="Tag Conversion Plan",
            message=(
                f"Repository         : {args.repository.display}\n"
                f"Operation          : {args.scope.value} tag replacement\n"
                f"Destination format : {plan.target_format.value}\n"
                f"Mode               : {mode}\n"
                f"Atomic mechanism   : {scope_description}\n"
                "Source tags        : replaced after destination validation\n"
                f"Planned            : {len(plan.conversions)}\n"
                f"Skipped            : {len(plan.skipped)}"
            ),
        )
    )
    if plan.conversions:
        console.print(_conversion_table(plan))
    if plan.skipped:
        console.print(_skipped_table(plan))


def _confirm_plan(*, args: ConvertTagsArgs, plan: TagConversionPlan) -> None:
    """Confirm a live local transaction or remote atomic push."""

    if args.dry_run or args.yes or not plan.conversions:
        return

    effect = (
        "replace the displayed local tag references in one transaction"
        if args.scope is TagConversionScope.LOCAL
        else (
            "atomically create the displayed destination remote tags and "
            "delete their source remote tags"
        )
    )
    console.print(warning_panel(f"This live operation will {effect}."))
    typer.confirm("Apply this tag replacement plan?", abort=True)


def _show_summary(
    *,
    args: ConvertTagsArgs,
    plan: TagConversionPlan,
    replaced_count: int,
) -> None:
    """Display an explicit local, remote, or dry-run result summary."""

    if args.dry_run:
        console.print(
            success_panel(
                f"Dry-run preview completed. Would replace {replaced_count} "
                "tag(s).\n\nNo tag objects, local refs, or remote refs were changed."
            )
        )
    elif replaced_count:
        console.print(
            success_panel(
                f"✅ Replaced {replaced_count} {args.scope.value} tag(s) atomically."
            )
        )
    else:
        console.print(warning_panel("No tag replacements were needed."))

    action = "Would replace" if args.dry_run else "Replaced"
    console.print(
        summary_panel(
            title=(
                "Tag Conversion Dry-Run Summary"
                if args.dry_run
                else "Tag Conversion Summary"
            ),
            message=(
                f"Repository         : {args.repository.display}\n"
                f"Operation          : {args.scope.value} tag replacement\n"
                f"Destination format : {plan.target_format.value}\n"
                f"Planned            : {len(plan.conversions)}\n"
                f"Skipped            : {len(plan.skipped)}\n"
                f"{action:<18} : {replaced_count}"
            ),
        )
    )


def _execute_conversion(*, args: ConvertTagsArgs, repository: Path) -> None:
    """Plan, preflight, confirm, and atomically apply one scoped conversion."""

    git = create_git_service(
        dry_run=args.dry_run,
        is_silent=args.silent,
        repository=repository,
    )
    with progress_task(
        "Preparing tag conversion",
        total=3,
        enabled=args.progress_enabled,
    ) as progress:
        progress.update("Validating target repository")
        _validate_repository(git)
        progress.advance()

        progress.update("Discovering repository tags")
        tags = git.get_all_tags()
        if not tags:
            console.print(warning_panel("⚠️ No tags found in the target repository."))
            raise typer.Exit(code=1)
        progress.advance()

        progress.update("Planning tag replacements")
        converter = TagConverter()
        plan = converter.plan_conversions(tags, args.target_format)
        progress.advance()

    replacement_service = TagReplacementService(git)

    _show_plan(args=args, plan=plan)
    collisions = [
        item
        for item in plan.skipped
        if item.reason.startswith("destination tag already exists")
    ]
    if collisions:
        console.print(
            error_panel(
                "Tag replacement stopped because one or more destination tag "
                "names already exist. Resolve every collision and rerun the plan."
            )
        )
        raise typer.Exit(code=1)

    try:
        with progress_spinner(
            "Validating source tag metadata",
            enabled=args.progress_enabled,
        ):
            prepared = replacement_service.prepare(
                plan.conversions,
                remote=args.scope is TagConversionScope.REMOTE,
            )
    except ReflowError as exc:
        console.print(error_panel(str(exc)))
        raise typer.Exit(code=1) from exc

    _confirm_plan(args=args, plan=plan)

    if not prepared or args.dry_run:
        _show_summary(args=args, plan=plan, replaced_count=len(prepared))
        return

    try:
        operation = (
            "Applying local tag transaction"
            if args.scope is TagConversionScope.LOCAL
            else "Applying guarded atomic remote push"
        )
        with progress_spinner(operation, enabled=args.progress_enabled):
            if args.scope is TagConversionScope.LOCAL:
                replacement_service.replace_local(prepared)
            else:
                replacement_service.replace_remote(prepared)
    except ReflowError as exc:
        logger.debug("Tag replacement failed: %s", exc, exc_info=True)
        console.print(error_panel(str(exc)))
        raise typer.Exit(code=1) from None

    _show_summary(args=args, plan=plan, replaced_count=len(prepared))


def run_convert_tags(
    ctx: typer.Context,
    *,
    scope: TagConversionScope,
    target_format: TagFormat | None = None,
    yes: bool | None = None,
) -> None:
    """Resolve a scoped target and run tag replacement in its checkout."""

    args = resolve_convert_tags_args(
        execution_args=ctx.obj.execution_args,
        scope=scope,
        target_format=target_format,
        yes=yes,
    )
    console.print(
        summary_panel(title="Target Repository", message=args.repository.display)
    )

    workspace = RepositoryWorkspace(
        args.repository,
        dry_run=args.dry_run,
        is_silent=args.silent,
        progress_enabled=args.progress_enabled,
    )
    with workspace.materialize() as repository:
        _execute_conversion(args=args, repository=repository)


@app.command("local")
@handle_cli_errors(
    "Local tag conversion",
    solution=(
        "Select a persistent local checkout, resolve destination collisions or "
        "signed tags, and preview the replacement with --dry-run."
    ),
)
def convert_local(
    ctx: typer.Context,
    target_format: TargetFormatOption = None,
    yes: YesOption = None,
) -> None:
    """Replace converted tag names only in a persistent local checkout."""

    run_convert_tags(
        ctx,
        scope=TagConversionScope.LOCAL,
        target_format=target_format,
        yes=yes,
    )


@app.command("remote")
@handle_cli_errors(
    "Remote tag conversion",
    solution=(
        "Verify the repository target, Git authentication, remote permissions, "
        "and atomic-push support, then preview with --dry-run."
    ),
)
def convert_remote(
    ctx: typer.Context,
    target_format: TargetFormatOption = None,
    yes: YesOption = None,
) -> None:
    """Atomically replace converted tag names on the configured Git remote."""

    run_convert_tags(
        ctx,
        scope=TagConversionScope.REMOTE,
        target_format=target_format,
        yes=yes,
    )

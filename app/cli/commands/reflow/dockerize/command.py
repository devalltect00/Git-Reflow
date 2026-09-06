# app/cli/commands/reflow/dockerize/command.py

"""
Docker image build and publishing command.

Command
-------
    reflow dockerize

Build and push Docker images for all repository tags.

This command:

    - Reads Docker configuration
    - Retrieves repository tags
    - Builds Docker images
    - Tags latest image
    - Pushes images
    - Optionally removes local images

Supported providers:

    - GitHub Container Registry (ghcr.io)
    - GitLab Container Registry
    - Both
"""

import logging
from pathlib import Path

import typer

from app.cli.commands.reflow.dockerize.models import DockerPublishFailure
from app.cli.commands.reflow.dockerize.resolver import resolve_dockerize_args
from app.cli.errors import handle_cli_errors
from app.cli.help import DOCKERIZE_HELP
from app.core.docker import create_docker_service
from app.core.git import GitService, create_git_service
from app.core.reflow import Dockerizer
from app.core.repository import RepositoryWorkspace
from app.core.shared import ReflowError
from app.core.shared.exceptions import ConfigurationError
from app.ui.console import console
from app.ui.panels import error_panel, success_panel, summary_panel, warning_panel
from app.ui.progress import create_progress, progress_spinner

logger = logging.getLogger(__name__)

app = typer.Typer(
    invoke_without_command=True,
    help="""
    Build and publish Docker images.

    Examples
    --------

        reflow dockerize

        reflow --dry-run dockerize
    """,
)


def _validate_repository(
    git: GitService,
) -> None:
    """
    Validate Git repository.

    Workflow:
        1. Check repository status.
        2. Raise CLI error if invalid.

    Args:
        git (GitService):
            Git service.

    Raises:
        typer.Exit:
            If repository is invalid.
    """
    if git.is_git_repo():
        return

    console.print(error_panel("Current directory is not a Git repository."))

    raise typer.Exit(
        code=1,
    )


def _publish_registry(
    *,
    dockerizer: Dockerizer,
    tags: list[str],
    image: str,
    keep_local_images: bool,
    progress_enabled: bool,
) -> tuple[list[str], list[DockerPublishFailure]]:
    """
    Publish images to a registry.

    Workflow:
        1. Discover tags.
        2. Publish tags.
        3. Track failures.
        4. Return results.

    Args:
        dockerizer (Dockerizer):
            Dockerizer instance.

        image (str):
            Registry image.

        keep_local_images (bool):
            Keep local images.

        progress_enabled (bool):
            Display per-tag Docker publishing progress.

    Returns:
        tuple[list[str], list[DockerPublishFailure]]:
            Published tags and structured failures.
    """
    published: list[str] = []
    failed: list[DockerPublishFailure] = []

    if not tags:
        return (
            published,
            failed,
        )

    latest_tag = tags[-1]

    with create_progress(enabled=progress_enabled) as progress:
        task = progress.add_task(
            f"Publishing {image}",
            total=len(tags),
        )

        for tag in tags:
            try:
                dockerizer.publish_tag(
                    image=image,
                    tag=tag,
                    latest_tag=latest_tag,
                    keep_local_images=keep_local_images,
                )

                published.append(
                    tag,
                )

            except ReflowError as exc:
                logger.debug(
                    "Failed Docker publication '%s:%s': %s",
                    image,
                    tag,
                    exc,
                    exc_info=True,
                )
                failed.append(
                    DockerPublishFailure(image=image, tag=tag, reason=str(exc))
                )

            progress.advance(
                task,
            )

    return (
        published,
        failed,
    )


def _show_summary(
    *,
    published: list[str],
    failed: list[DockerPublishFailure],
    dry_run: bool = False,
) -> None:
    """
    Display publishing summary.

    Workflow:
        1. Show success summary.
        2. Show failed tags.
        3. Show final totals.

    Args:
        published (list[str]):
            Published tags.

        failed (list[DockerPublishFailure]):
            Failed image-tag publications and their reasons.

        dry_run (bool):
            Display planned operations instead of completed publications.
    """
    console.print()

    if dry_run and not failed:
        console.print(
            success_panel(
                f"Dry-run preview completed. Would publish {len(published)} tag(s).\n\n"
                "No Docker images were built, pushed, tagged, or removed."
            )
        )
    elif not failed:
        console.print(success_panel(f"Published {len(published)} tag(s)."))

    if failed:
        details = "\n".join(
            f"- {failure.image}:{failure.tag}\n  {failure.reason}" for failure in failed
        )
        message = (
            f"Failed to {'preview' if dry_run else 'publish'} "
            f"{len(failed)} image tag(s).\n\n{details}\n\n"
            "Check that Docker is running, the target contains a usable "
            "Dockerfile, the build context is valid, and registry "
            "authentication is configured."
        )
        panel = warning_panel if published else error_panel
        console.print(panel(message))

    console.print(
        summary_panel(
            title=(
                "Docker Publish Dry-Run Summary"
                if dry_run
                else "Docker Publish Summary"
            ),
            message=(
                f"Would publish     : {len(published)}\n"
                f"Failed to preview : {len(failed)}"
                if dry_run
                else f"Published : {len(published)}\nFailed    : {len(failed)}"
            ),
        )
    )


def _show_configuration(
    *,
    repository,
    provider: str,
    github_image: str | None,
    gitlab_image: str | None,
) -> None:
    """
    Display resolved Docker configuration.

    Workflow:
        1. Show selected provider.
        2. Show configured registries.
        3. Show image names.
    """

    lines: list[str] = [
        f"Repository : {repository}",
        f"Provider : {provider}",
    ]

    if provider in ("github", "both") and github_image:
        lines.append(f"GitHub   : {github_image}")

    if provider in ("gitlab", "both") and gitlab_image:
        lines.append(f"GitLab   : {gitlab_image}")

    console.print(
        summary_panel(
            title="Docker Configuration",
            message="\n".join(lines),
        )
    )


def _validate_tags(
    tags: list[str],
) -> list[str]:
    """
    Validate repository tags.

    Workflow:
        1. Ensure tags exist.
        2. Return tags.
    """
    if tags:
        return tags

    console.print(warning_panel("No Git tags found."))

    raise typer.Exit(
        code=1,
    )


def _execute_dockerize(
    *,
    args,
    repository: Path,
) -> None:
    """
    Execute Docker publishing in a materialized repository.

    Args:
        args:
            Resolved Docker publishing arguments.

        repository:
            Existing local checkout or managed temporary clone.
    """

    with progress_spinner(
        "Inspecting Docker publishing target",
        enabled=args.progress_enabled,
    ):
        git = create_git_service(
            dry_run=args.dry_run,
            is_silent=args.silent,
            repository=repository,
        )
        docker = create_docker_service(
            dry_run=args.dry_run,
            is_silent=args.silent,
            repository=repository,
        )

        _validate_repository(git)
        dockerizer = Dockerizer(git=git, docker=docker)
        tags = _validate_tags(tags=git.get_all_tags())

    published: list[str] = []
    failed: list[DockerPublishFailure] = []

    if args.provider in ("github", "both"):
        if args.github_image is None:
            raise ConfigurationError("GitHub image should have been validated.")

        successful, unsuccessful = _publish_registry(
            dockerizer=dockerizer,
            tags=tags,
            image=args.github_image,
            keep_local_images=args.keep_local_images,
            progress_enabled=args.progress_enabled,
        )
        published.extend(successful)
        failed.extend(unsuccessful)

    if args.provider in ("gitlab", "both"):
        if args.gitlab_image is None:
            raise ConfigurationError("GitLab image should have been validated.")

        successful, unsuccessful = _publish_registry(
            dockerizer=dockerizer,
            tags=tags,
            image=args.gitlab_image,
            keep_local_images=args.keep_local_images,
            progress_enabled=args.progress_enabled,
        )
        published.extend(successful)
        failed.extend(unsuccessful)

    _show_summary(
        published=published,
        failed=failed,
        dry_run=args.dry_run,
    )

    if failed:
        raise typer.Exit(code=1)


def run_dockerize(
    ctx: typer.Context,
) -> None:
    """
    Execute docker publishing workflow.

    Workflow:
        1. Resolve arguments.
        2. Create services.
        3. Validate repository.
        4. Publish configured registries.
        5. Display summary.

    Args:
        ctx (typer.Context):
            Typer context.
    """
    execution_args = ctx.obj.execution_args

    args = resolve_dockerize_args(
        execution_args=execution_args,
    )

    _show_configuration(
        repository=args.repository.display,
        provider=args.provider,
        github_image=args.github_image,
        gitlab_image=args.gitlab_image,
    )

    workspace = RepositoryWorkspace(
        args.repository,
        dry_run=args.dry_run,
        is_silent=args.silent,
        progress_enabled=args.progress_enabled,
    )
    with workspace.materialize() as repository:
        _execute_dockerize(args=args, repository=repository)


@app.callback(
    help=DOCKERIZE_HELP,
)
@handle_cli_errors(
    "Docker publishing",
    solution=(
        "Verify repository access and ownership, then confirm that Docker is "
        "installed and running, the selected tag contains a usable Dockerfile, "
        "the build context is valid, and registry authentication is configured. "
        "Preview with --dry-run before retrying."
    ),
)
def dockerize(
    ctx: typer.Context,
) -> None:
    """
    Build and publish Docker images.
    """
    run_dockerize(
        ctx,
    )

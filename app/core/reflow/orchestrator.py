# app/core/reflow/orchestrator.py

"""
Reflow orchestration layer.

This module coordinates the Reflow workflow.

Responsibilities:
- Validate repository state
- Retrieve tags
- Filter tags
- Check GitHub releases
- Re-push tags to trigger workflows

This module coordinates services but does not execute
Git, GitHub, or Docker commands directly.
"""

import logging
import time
from pathlib import Path

from app.core.git.factory import create_git_service
from app.core.github.factory import create_github_service
from app.core.reflow.tag_processor import TagProcessor
from app.core.shared import ReflowError
from app.theme import theme
from app.ui.console import console
from app.ui.progress import create_progress

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Main Reflow workflow coordinator.

    This class coordinates:
    - Git operations
    - GitHub operations
    - Tag processing

    It does not contain low-level command execution.
    """

    def __init__(
        self,
        dry_run: bool = False,
        is_silent: bool = False,
        delay: int = 2,
        repository: Path | None = None,
        progress_enabled: bool = True,
    ) -> None:
        """
        Initialize orchestrator.

        Args:
            dry_run (bool):
                Enable dry-run mode.

            is_silent (bool):
                Disable command logging.

            delay (int):
                Delay between GitHub workflow triggers.

            repository (Path | None):
                Repository whose tags and releases are recovered.

            progress_enabled (bool):
                Display per-tag release-recovery progress.
        """
        self.git = create_git_service(
            dry_run=dry_run,
            is_silent=is_silent,
            repository=repository,
        )

        self.github = create_github_service(
            dry_run=dry_run,
            is_silent=is_silent,
            repository=repository,
        )

        self.processor = TagProcessor()

        self.delay = delay
        self.dry_run = dry_run
        self.repository = (repository or Path.cwd()).resolve()
        self.progress_enabled = progress_enabled

    # =====================================================
    # Public API
    # =====================================================

    def run(
        self,
        only_stable: bool = False,
        limit: int | None = None,
    ) -> bool:
        """
        Run the Reflow process.

        Args:
            only_stable (bool):
                Process only stable tags.

            limit (int | None):
                Limit the number of processed tags.

        Returns:
            bool:
                True when discovery and every selected tag succeed; otherwise
                False for a handled operational failure.
        """
        logger.info("Starting release recovery%s", " preview" if self.dry_run else "")

        operation_name = (
            "release recovery preview" if self.dry_run else "release recovery"
        )
        console.print(f"[{theme.primary}]🚀 Starting {operation_name}...[/]")

        if not self.git.is_git_repo():
            logger.debug("Current directory is not a Git repository.")

            console.print("[red]❌ Current directory is not a Git repository.[/red]")
            return False

        tags = self.git.get_all_tags()

        logger.info("Found %s tags", len(tags))

        tags = self.processor.filter_valid_tags(tags)

        logger.info("Found %s valid tags", len(tags))

        if only_stable:
            tags = self.processor.filter_stable_tags(tags)

            logger.info(
                "Filtered to %s stable tags",
                len(tags),
            )

        if limit:
            tags = tags[:limit]

            logger.info(
                "Applying limit=%s (%s tags)",
                limit,
                len(tags),
            )

        if not tags:
            logger.warning("No tags to process")

            console.print("[yellow]⚠️ No tags to process.[/yellow]")
            return True

        failed_tags: list[tuple[str, str]] = []

        with create_progress(enabled=self.progress_enabled) as progress:
            task = progress.add_task(
                "Processing release tags",
                total=len(tags),
            )

            for tag in tags:
                progress.update(
                    task,
                    description=f"Processing {tag}",
                )

                try:
                    self._process_tag(tag)

                except ReflowError as exc:
                    logger.debug(
                        "Failed release tag '%s': %s",
                        tag,
                        exc,
                        exc_info=True,
                    )

                    failed_tags.append((tag, str(exc)))

                progress.advance(task)

        if failed_tags:
            logger.debug(
                "Failed tags: %s",
                failed_tags,
            )

            details = "\n".join(f"- {tag}: {reason}" for tag, reason in failed_tags)
            console.print(f"[yellow]⚠️ Failed tags:\n{details}[/yellow]")
            return False

        else:
            if self.dry_run:
                logger.info("Release recovery preview completed successfully")
                console.print(
                    "[green]Dry-run preview completed successfully. "
                    "No remote tags were deleted or pushed.[/green]"
                )
            else:
                logger.info("Release recovery completed successfully")
                console.print(
                    "[green]🎉 Release recovery completed successfully![/green]"
                )

        return True

    # =====================================================
    # Internal
    # =====================================================

    def _process_tag(
        self,
        tag: str,
    ) -> None:
        """
        Process a single tag.

        Workflow:
            1. Check release existence
            2. Delete remote tag
            3. Push tag again
            4. Wait before next tag

        Args:
            tag (str):
                Tag name.
        """
        logger.info(
            "Processing tag '%s'",
            tag,
        )

        if self.github.release_exists(tag):
            logger.info(
                "Skipping '%s' (release already exists)",
                tag,
            )
            return

        logger.debug(
            "Deleting remote tag '%s'",
            tag,
        )

        self.git.delete_remote_tag(tag)

        logger.debug(
            "Re-pushing tag '%s'",
            tag,
        )

        self.git.push_tag(tag)

        logger.debug(
            "Waiting %s seconds",
            self.delay,
        )

        if not self.dry_run:
            time.sleep(self.delay)

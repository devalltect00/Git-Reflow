# app/core/repository/workspace.py

"""
Managed repository workspace lifecycle.

Responsibilities:
- Yield validated local repositories without copying
- Clone remote repositories into temporary working directories
- Remove temporary clones after success or failure
"""

import logging
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from app.core.repository.executor import RepositoryExecutor
from app.core.repository.target import RepositoryTarget
from app.core.shared import RepositoryOperationError
from app.ui.progress import progress_spinner

logger = logging.getLogger(__name__)


class RepositoryWorkspace:
    """Materialize a repository target for one command invocation."""

    def __init__(
        self,
        target: RepositoryTarget,
        *,
        dry_run: bool = False,
        is_silent: bool = False,
        progress_enabled: bool = True,
        executor: RepositoryExecutor | None = None,
    ) -> None:
        """
        Initialize workspace management.

        Args:
            target:
                Validated local or remote repository target.

            dry_run:
                Shared dry-run state used by clone command logging.

            is_silent:
                Suppress clone command logging.

            progress_enabled:
                Display repository materialization progress.

            executor:
                Optional clone executor for dependency injection.
        """

        self.target = target
        self.progress_enabled = progress_enabled
        self.executor = executor or RepositoryExecutor(
            dry_run=dry_run,
            is_silent=is_silent,
        )

    @contextmanager
    def materialize(self) -> Iterator[Path]:
        """
        Yield a concrete local working tree for the target.

        Yields:
            Path:
                Existing local target or temporary remote clone.

        Raises:
            RepositoryOperationError:
                If the remote repository cannot be cloned.
        """

        if self.target.path is not None:
            yield self.target.path
            return

        repository_url = self.target.url

        if repository_url is None:
            raise RepositoryOperationError("Remote repository URL is unavailable.")

        logger.info("Materializing remote repository '%s'", repository_url)

        with tempfile.TemporaryDirectory(prefix="reflow-repository-") as root:
            checkout = Path(root) / "checkout"
            try:
                with progress_spinner(
                    "Cloning target repository",
                    enabled=self.progress_enabled,
                ):
                    result = self.executor.clone(
                        url=repository_url,
                        destination=checkout,
                    )
            except OSError as exc:
                logger.debug("Unable to execute Git clone: %s", exc, exc_info=True)
                raise RepositoryOperationError(
                    "Unable to execute Git clone. Verify that Git is installed "
                    "and available on PATH."
                ) from exc

            if not result.success:
                logger.debug(
                    "Failed to materialize remote repository '%s'",
                    repository_url,
                )
                raise RepositoryOperationError(
                    f"Failed to clone repository '{repository_url}'. "
                    "Verify the URL and Git authentication."
                )

            logger.info("Remote repository materialized successfully")

            try:
                yield checkout.resolve()
            finally:
                logger.debug("Cleaning temporary repository workspace")

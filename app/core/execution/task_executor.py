# app/core/execution/task_executor.py

"""
Task execution utilities.

This module provides a reusable task executor that supports:
- Parallel execution
- Retry handling
- Progress tracking

This executor is generic and can be used by any workflow.

It is not tied to:
- Git
- GitHub
- Docker
- Reflow
"""

import logging
import time
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
)

logger = logging.getLogger(__name__)


class TaskExecutor:
    """
    Execute tasks in parallel.

    Features:
    - Thread pool execution
    - Retry support
    - Progress display
    """

    def __init__(
        self,
        max_workers: int = 4,
        retries: int = 2,
    ) -> None:
        """
        Initialize task executor.

        Args:
            max_workers (int):
                Maximum worker threads.

            retries (int):
                Number of retries per task.
        """
        self.max_workers = max_workers
        self.retries = retries

    def run(
        self,
        func,
        items: list,
    ) -> None:
        """
        Execute tasks in parallel.

        Args:
            func:
                Function to execute.

            items (list):
                Items to process.
        """
        failed_items = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
        ) as progress:
            task = progress.add_task(
                "⚡ Processing...",
                total=len(items),
            )

            with ThreadPoolExecutor(
                max_workers=self.max_workers,
            ) as executor:
                future_map = {
                    executor.submit(
                        self._execute_with_retry,
                        func,
                        item,
                    ): item
                    for item in items
                }

                for future in as_completed(future_map):
                    item = future_map[future]

                    try:
                        future.result()

                    except Exception as exc:
                        logger.error(
                            "Failed to process '%s': %s",
                            item,
                            exc,
                        )

                        failed_items.append(item)

                    progress.advance(task)

        if failed_items:
            logger.warning(
                "Failed items (%s): %s",
                len(failed_items),
                failed_items,
            )

    def _execute_with_retry(
        self,
        func,
        item,
    ):
        """
        Execute a task with retry support.

        Args:
            func:
                Function to execute.

            item:
                Item passed to the function.

        Returns:
            Any:
                Function result.
        """
        for attempt in range(self.retries + 1):
            try:
                return func(item)

            except Exception as exc:
                logger.error(
                    "Error processing '%s' (attempt %s): %s",
                    item,
                    attempt + 1,
                    exc,
                )

                time.sleep(1)

        raise RuntimeError(f"Failed permanently: {item}")

"""
Execution engine with:
- parallel processing
- retry support
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


class Executor:
    """
    Handles execution with concurrency and retry.
    """

    def __init__(self, max_workers: int = 4, retries: int = 2):
        self.max_workers = max_workers
        self.retries = retries

    def run(self, func, items: list):
        """
        Run tasks in parallel.

        Args:
            func: function to execute
            items: list of items
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self._wrap, func, item) for item in items]

            for future in as_completed(futures):
                future.result()

    def _wrap(self, func, item):
        """
        Retry wrapper.
        """
        for attempt in range(self.retries + 1):
            try:
                return func(item)
            except Exception as e:
                logger.error(f"❌ Error on {item} (attempt {attempt+1}): {e}")
                time.sleep(1)

        logger.error(f"💥 Failed permanently: {item}")
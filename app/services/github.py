"""
GitHub service using gh CLI.

Used for:
- Checking if release exists
"""

import logging
import subprocess

logger = logging.getLogger(__name__)


class GitHubService:
    """
    GitHub integration via gh CLI.
    """

    def release_exists(self, tag: str) -> bool:
        """
        Check if GitHub release already exists.

        Args:
            tag (str)

        Returns:
            bool
        """
        try:
            result = subprocess.run(
                ["gh", "release", "view", tag],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            exists = result.returncode == 0

            if exists:
                logger.info(f"⏭ Skipping (already released): {tag}")

            return exists

        except Exception as e:
            logger.warning(f"⚠️ Failed to check release for {tag}: {e}")
            return False
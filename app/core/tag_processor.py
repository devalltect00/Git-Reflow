"""
Tag processing utilities.

Handles:
- Validation
- Filtering
"""

import logging
import re

logger = logging.getLogger(__name__)


class TagProcessor:
    """
    Processes and validates Git tags.
    """

    TAG_REGEX = re.compile(
        r"^v[0-9]+\.[0-9]+\.[0-9]+([.-][0-9A-Za-z.]+)?$"
    )

    def is_valid(self, tag: str) -> bool:
        """
        Check if tag matches expected format.

        Args:
            tag (str): Git tag

        Returns:
            bool: True if valid
        """
        return bool(self.TAG_REGEX.match(tag))

    def filter_valid_tags(self, tags: list[str]) -> list[str]:
        """
        Filter only valid tags.

        Args:
            tags (list[str])

        Returns:
            list[str]
        """
        valid = []

        for tag in tags:
            if self.is_valid(tag):
                valid.append(tag)
            else:
                logger.warning(f"⚠️ Skipping invalid tag: {tag}")

        return valid
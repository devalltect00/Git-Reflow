# app/core/reflow/tag_processor.py

"""
Tag processing utilities.

This module contains helper functions for working with Git tags.

Responsibilities:
- Validate tags
- Filter valid tags
- Filter stable tags

This module contains only domain logic and does not depend on:
- Git
- GitHub
- Docker
- CLI
- Rich
"""

import logging
import re

logger = logging.getLogger(__name__)


class TagProcessor:
    """
    Processes and validates Git tags.

    This class contains simple tag-related business rules used
    by Reflow.
    """

    TAG_REGEX = re.compile(r"^v[0-9]+\.[0-9]+\.[0-9]+([.-][0-9A-Za-z.]+)?$")

    def is_valid(self, tag: str) -> bool:
        """
        Check if tag is valid and matches expected format.

        Examples:
            v1.0.0
            v1.2.3
            v1.2.3-rc1
            v1.2.3-beta.1

        Args:
            tag (str):
                Git tag.

        Returns:
            bool:
                True if the tag matches the expected format.
        """
        return bool(self.TAG_REGEX.match(tag))

    def is_stable(
        self,
        tag: str,
    ) -> bool:
        """
        Check whether a tag is a stable release.

        Stable tags do not contain pre-release markers.

        Examples:
            v1.0.0        -> True
            v1.2.3        -> True
            v1.2.3-rc1    -> False
            v1.2.3-beta1  -> False

        Args:
            tag (str):
                Tag name.

        Returns:
            bool:
                True if the tag is stable.
        """
        return "-" not in tag

    def filter_valid_tags(self, tags: list[str]) -> list[str]:
        """
        Filter only valid tags.

        Args:
            tags (list[str]):
                Tags to evaluate.

        Returns:
            list[str]:
                Valid tags only.
        """
        valid_tags: list[str] = []

        for tag in tags:
            if self.is_valid(tag):
                valid_tags.append(tag)
            else:
                # logger.warning(f"⚠️ Skipping invalid tag: {tag}")
                logger.warning(
                    "Skipping invalid tag '%s'",
                    tag,
                )

        return valid_tags

    def filter_stable_tags(
        self,
        tags: list[str],
    ) -> list[str]:
        """
        Filter stable tags.

        Args:
            tags (list[str]):
                Tags to evaluate.

        Returns:
            list[str]:
                Stable tags only.
        """
        return [tag for tag in tags if self.is_stable(tag)]

    def filter_valid_stable_tags(
        self,
        tags: list[str],
    ) -> list[str]:
        """
        Filter tags that are both valid and stable.

        Args:
            tags (list[str]):
                Tags to evaluate.

        Returns:
            list[str]:
                Valid stable tags only.
        """
        return [tag for tag in tags if self.is_valid(tag) and self.is_stable(tag)]

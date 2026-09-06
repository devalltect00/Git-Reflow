# tests/core/reflow/test_dockerizer.py

"""
Tests for Dockerizer.
"""

from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

from app.core.reflow import Dockerizer


class TestDockerizer:
    """
    Tests for Dockerizer.
    """

    @pytest.fixture
    def git(self):
        git = MagicMock()
        git.tag_worktree.return_value.__enter__.return_value = Path("tag-worktree")
        return git

    @pytest.fixture
    def docker(self):
        return Mock()

    @pytest.fixture
    def dockerizer(
        self,
        git,
        docker,
    ):
        return Dockerizer(
            git=git,
            docker=docker,
        )

    # =====================================================
    # publish_tag
    # =====================================================

    def test_publish_tag(
        self,
        dockerizer,
        docker,
    ):
        """
        Should build and push image.
        """
        dockerizer.publish_tag(
            image="ghcr.io/test/app",
            tag="v1.0.0",
            latest_tag="v2.0.0",
        )

        docker.build_image.assert_called_once()
        assert docker.build_image.call_args.kwargs["context"] == Path("tag-worktree")
        docker.push_image.assert_called_once()

    def test_publish_latest_tag(
        self,
        dockerizer,
        docker,
    ):
        """
        Should create latest tag.
        """
        dockerizer.publish_tag(
            image="ghcr.io/test/app",
            tag="v2.0.0",
            latest_tag="v2.0.0",
        )

        docker.tag_image.assert_called_once()

        assert docker.push_image.call_count == 2

    def test_keep_local_images(
        self,
        dockerizer,
        docker,
    ):
        """
        Should keep local images.
        """
        dockerizer.publish_tag(
            image="ghcr.io/test/app",
            tag="v1.0.0",
            latest_tag="v2.0.0",
            keep_local_images=True,
        )

        docker.remove_local_image.assert_not_called()

    def test_remove_local_images(
        self,
        dockerizer,
        docker,
    ):
        """
        Should remove local images.
        """
        dockerizer.publish_tag(
            image="ghcr.io/test/app",
            tag="v1.0.0",
            latest_tag="v2.0.0",
            keep_local_images=False,
        )

        docker.remove_local_image.assert_called_once()

    # =====================================================
    # publish_all_tags
    # =====================================================

    def test_publish_all_tags(
        self,
        dockerizer,
        git,
    ):
        """
        Should publish all tags.
        """
        git.get_all_tags.return_value = [
            "v1.0.0",
            "v2.0.0",
        ]

        result = dockerizer.publish_all_tags(
            image="ghcr.io/test/app",
        )

        assert result == [
            "v1.0.0",
            "v2.0.0",
        ]

    def test_publish_all_tags_returns_empty_list(
        self,
        dockerizer,
        git,
    ):
        """
        Should return empty list when no tags exist.
        """
        git.get_all_tags.return_value = []

        result = dockerizer.publish_all_tags(
            image="ghcr.io/test/app",
        )

        assert result == []

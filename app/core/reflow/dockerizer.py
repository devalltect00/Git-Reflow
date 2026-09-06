# app/core/reflow/dockerizer.py

"""
Docker image publishing workflow.

This module contains the Docker publishing workflow used
by the reflow dockerize command.
"""

from __future__ import annotations

import logging

from app.core.docker import DockerService
from app.core.git import GitService

logger = logging.getLogger(__name__)


class Dockerizer:
    """
    Build and publish Docker images.

    Responsibilities:

    - Build images
    - Tag latest images
    - Push images
    - Cleanup local images
    """

    def __init__(
        self,
        git: GitService,
        docker: DockerService,
    ) -> None:
        """
        Initialize Dockerizer.

        Args:
            git (GitService):
                Git service.

            docker (DockerService):
                Docker service.
        """
        self.git = git
        self.docker = docker

    def publish_tag(
        self,
        *,
        image: str,
        tag: str,
        latest_tag: str,
        keep_local_images: bool = False,
    ) -> None:
        """
        Publish a Docker image for a tag.

        Workflow:
            1. Build image.
            2. Tag latest image if applicable.
            3. Push image.
            4. Push latest image if applicable.
            5. Remove local image if configured.

        Args:
            image (str):
                Docker image name.

            tag (str):
                Git tag.

            latest_tag (str):
                Latest repository tag.

            keep_local_images (bool):
                Keep local images after push.

        Returns:
            None
        """
        clean_tag = tag.lstrip("v")

        logger.info(
            "Publishing image '%s:%s'",
            image,
            clean_tag,
        )

        with self.git.tag_worktree(tag) as build_context:
            self.docker.build_image(
                image,
                clean_tag,
                context=build_context,
            )

            if tag == latest_tag:
                self.docker.tag_image(
                    image,
                    clean_tag,
                    "latest",
                )

            self.docker.push_image(
                image,
                clean_tag,
            )

            if tag == latest_tag:
                self.docker.push_image(
                    image,
                    "latest",
                )

            if tag != latest_tag and not keep_local_images:
                self.docker.remove_local_image(
                    image,
                    clean_tag,
                )

    def publish_all_tags(
        self,
        *,
        image: str,
        keep_local_images: bool = False,
    ) -> list[str]:
        """
        Publish Docker images for all tags.

        Workflow:
            1. Discover repository tags.
            2. Determine latest tag.
            3. Publish all tags.
            4. Return processed tags.

        Args:
            image (str):
                Docker image name.

            keep_local_images (bool):
                Keep local images after push.

        Returns:
            list[str]:
                Published tags.
        """
        tags = self.git.get_all_tags()

        if not tags:
            return []

        latest_tag = tags[-1]

        for tag in tags:
            self.publish_tag(
                image=image,
                tag=tag,
                latest_tag=latest_tag,
                keep_local_images=keep_local_images,
            )

        return tags

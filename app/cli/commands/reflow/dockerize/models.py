# app/cli/commands/reflow/dockerize/models.py

"""
Argument models for:

    reflow dockerize

These models represent fully-resolved and validated
arguments ready for backend execution.
"""

from dataclasses import dataclass

from app.cli.commands.reflow.common.models import ReflowExecutionArgs


@dataclass(slots=True)
class DockerizeArgs(ReflowExecutionArgs):
    """
    Dockerize command arguments.

    All values have already been resolved from:

        CLI
            ↓
        Config
            ↓
        Defaults

    Attributes
    ----------
    provider:
        Registry provider.

    github_image:
        GitHub image name.

    gitlab_image:
        GitLab image name.

    keep_local_images:
        Keep local images after push.
    """

    provider: str

    github_image: str | None

    gitlab_image: str | None

    keep_local_images: bool


@dataclass(frozen=True, slots=True)
class DockerPublishFailure:
    """Describe one failed image-tag publication attempt."""

    image: str
    tag: str
    reason: str

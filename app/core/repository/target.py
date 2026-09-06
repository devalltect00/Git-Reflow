# app/core/repository/target.py

"""
Repository target model.

Responsibilities:
- Resolve local-path and remote-URL repository targets
- Normalize local paths before workflow execution
- Validate remote Git URL syntax without performing network access
- Enforce mutually exclusive target selection
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from app.core.shared import ConfigurationError

_SUPPORTED_URL_SCHEMES = frozenset({"git", "http", "https", "ssh"})
_SCP_STYLE_URL = re.compile(r"^(?P<user>[^@\s]+)@(?P<host>[^:\s]+):(?P<path>[^\s]+)$")


@dataclass(frozen=True, slots=True)
class RepositoryTarget:
    """
    Validated local or remote repository target.

    Local targets reference existing directories. Remote targets retain a
    credential-free Git URL and are materialized later by
    :class:`RepositoryWorkspace` for the lifetime of a command.
    """

    path: Path | None = None
    url: str | None = None

    def __post_init__(self) -> None:
        """
        Validate the target invariant.

        Raises:
            ConfigurationError:
                If neither or both target forms are populated.
        """

        if (self.path is None) == (self.url is None):
            raise ConfigurationError(
                "Repository target must define exactly one of 'path' or 'url'."
            )

    @property
    def is_local(self) -> bool:
        """Return whether the target is an existing local directory."""

        return self.path is not None

    @property
    def is_remote(self) -> bool:
        """Return whether the target requires a managed temporary clone."""

        return self.url is not None

    @property
    def display(self) -> str:
        """Return a safe user-facing target description."""

        return str(self.path) if self.path is not None else str(self.url)

    def require_local(self, *, command: str) -> Path:
        """
        Return the local path or reject URL mode for a local-only command.

        Args:
            command:
                Command name included in the remediation message.

        Returns:
            Path:
                Validated local repository path.

        Raises:
            ConfigurationError:
                If the selected target is a remote URL.
        """

        if self.path is None:
            raise ConfigurationError(
                f"'{command}' requires a local repository path. "
                "Clone the repository first and use --repository or -C."
            )

        return self.path

    @classmethod
    def resolve(
        cls,
        value: str | Path | None = None,
        *,
        url: str | None = None,
        base_directory: Path | None = None,
    ) -> RepositoryTarget:
        """
        Resolve and validate one repository target.

        Args:
            value:
                Local CLI or configuration value. ``None`` resolves to ``.``
                only when ``url`` is also absent.

            url:
                Remote Git URL. Cannot be combined with ``value``.

            base_directory:
                Directory used to resolve relative local paths. Defaults to the
                current working directory.

        Returns:
            RepositoryTarget:
                Validated local or remote target.

        Raises:
            ConfigurationError:
                If target selection or validation fails.
        """

        if value is not None and url is not None:
            raise ConfigurationError(
                "Repository 'path' and 'url' are mutually exclusive. Choose one."
            )

        if url is not None:
            normalized_url = url.strip()
            cls._validate_url(normalized_url)
            return cls(url=normalized_url)

        base = (base_directory or Path.cwd()).resolve()
        path = Path(value or ".").expanduser()

        if not path.is_absolute():
            path = base / path

        path = path.resolve()

        if not path.exists():
            raise ConfigurationError(f"Repository path does not exist: {path}")

        if not path.is_dir():
            raise ConfigurationError(f"Repository path is not a directory: {path}")

        return cls(path=path)

    @staticmethod
    def _validate_url(value: str) -> None:
        """
        Validate a credential-safe remote Git URL.

        Args:
            value:
                URL supplied by CLI or configuration.

        Raises:
            ConfigurationError:
                If the URL is empty, malformed, unsupported, or contains
                embedded credentials.
        """

        if not value or any(character.isspace() for character in value):
            raise ConfigurationError("Repository URL is empty or contains spaces.")

        if _SCP_STYLE_URL.fullmatch(value):
            return

        parsed = urlparse(value)

        if parsed.scheme.lower() not in _SUPPORTED_URL_SCHEMES:
            supported = ", ".join(sorted(_SUPPORTED_URL_SCHEMES))
            raise ConfigurationError(
                f"Unsupported repository URL scheme. Expected one of: {supported}."
            )

        if not parsed.hostname or not parsed.path.strip("/"):
            raise ConfigurationError(
                "Repository URL must include a host and repository path."
            )

        if parsed.password is not None:
            raise ConfigurationError(
                "Repository URL must not contain embedded credentials."
            )

        if parsed.scheme.lower() in {"http", "https"} and parsed.username:
            raise ConfigurationError(
                "Repository URL must not contain embedded credentials."
            )

        if parsed.query or parsed.fragment:
            raise ConfigurationError(
                "Repository URL must not contain query parameters or fragments."
            )

# app/core/reflow/tag_replacement.py

"""Metadata-aware local and remote Git tag replacement workflows."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.core.git import GitService, TagRefReplacement, TagSnapshot
from app.core.reflow.tag_converter import TagConversion
from app.core.shared.exceptions import GitOperationError

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PreparedTagReplacement:
    """One planned conversion paired with its immutable source metadata."""

    conversion: TagConversion
    snapshot: TagSnapshot


class TagReplacementService:
    """Prepare and atomically apply tag-name replacements.

    Name-format conversion remains the responsibility of ``TagConverter``.
    This service owns source metadata inspection, signature safeguards, local
    transactions, remote atomic pushes, and post-operation verification.
    """

    def __init__(self, git: GitService) -> None:
        """Initialize the service with a repository-scoped Git service."""

        self.git = git

    def prepare(
        self,
        conversions: tuple[TagConversion, ...],
        *,
        remote: bool,
    ) -> tuple[PreparedTagReplacement, ...]:
        """Capture source metadata and validate local or remote preconditions."""

        prepared: list[PreparedTagReplacement] = []
        for conversion in conversions:
            snapshot = self.git.get_tag_snapshot(conversion.source)
            if snapshot.is_signed:
                raise GitOperationError(
                    f"Tag '{conversion.source}' is signed. Reflow cannot rename "
                    "it without invalidating the signature."
                )

            if remote:
                source_oid = self.git.get_remote_tag_oid(conversion.source)
                destination_oid = self.git.get_remote_tag_oid(conversion.destination)
                if source_oid != snapshot.ref_oid:
                    raise GitOperationError(
                        f"Remote source tag '{conversion.source}' changed or is "
                        "missing. Refresh the plan before retrying."
                    )
                if destination_oid is not None:
                    raise GitOperationError(
                        f"Remote destination tag already exists: "
                        f"{conversion.destination}."
                    )

            prepared.append(
                PreparedTagReplacement(
                    conversion=conversion,
                    snapshot=snapshot,
                )
            )

        return tuple(prepared)

    def replace_local(
        self,
        prepared: tuple[PreparedTagReplacement, ...],
    ) -> list[TagRefReplacement]:
        """Replace all planned local refs in one Git reference transaction."""

        replacements = self._materialize(prepared)
        self.git.replace_local_tags_atomically(replacements)
        logger.info("Replaced %s local tag(s) atomically", len(replacements))
        return replacements

    def replace_remote(
        self,
        prepared: tuple[PreparedTagReplacement, ...],
    ) -> list[TagRefReplacement]:
        """Replace all planned remote refs in one guarded atomic push."""

        replacements = self._materialize(prepared)
        self.git.replace_remote_tags_atomically(replacements)
        logger.info("Replaced %s remote tag(s) atomically", len(replacements))
        return replacements

    def _materialize(
        self,
        prepared: tuple[PreparedTagReplacement, ...],
    ) -> list[TagRefReplacement]:
        """Create destination tag objects without changing any tag reference."""

        return [
            self.git.create_replacement_ref(
                snapshot=item.snapshot,
                destination=item.conversion.destination,
            )
            for item in prepared
        ]

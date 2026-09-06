# app/core/git/models.py

"""Models for metadata-aware Git tag replacement operations."""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.core.shared.exceptions import GitOperationError

_SIGNATURE_MARKER = re.compile(
    r"^-----BEGIN (?:PGP|SSH) SIGNATURE-----$",
    flags=re.MULTILINE,
)


@dataclass(frozen=True, slots=True)
class TagSnapshot:
    """Immutable source-tag state captured before a replacement.

    Annotated tags retain their raw Git tag object so the target object, target
    type, tagger identity, tagger timestamp, timezone, message, and optional
    encoding header can be reconstructed under a new tag name. Lightweight tags
    have no tag object and retain only their referenced object ID.
    """

    name: str
    ref_oid: str
    object_type: str
    raw_object: str | None = None

    @property
    def is_annotated(self) -> bool:
        """Return whether the source reference points to an annotated tag."""

        return self.object_type == "tag"

    @property
    def is_signed(self) -> bool:
        """Return whether the annotated object contains a known signature."""

        return bool(self.raw_object and _SIGNATURE_MARKER.search(self.raw_object))

    def renamed_raw_object(self, destination: str) -> str:
        """Return the annotated tag object with only its tag header renamed.

        Args:
            destination:
                New Git tag name.

        Returns:
            str:
                Raw annotated-tag object suitable for ``git mktag``.

        Raises:
            GitOperationError:
                If the source is lightweight, signed, or malformed.
        """

        if not self.is_annotated or self.raw_object is None:
            raise GitOperationError(
                f"Tag '{self.name}' is lightweight and has no annotated object."
            )

        if self.is_signed:
            raise GitOperationError(
                f"Tag '{self.name}' is signed. Renaming changes the signed payload; "
                "Reflow will not remove or invalidate its signature."
            )

        header, separator, message = self.raw_object.partition("\n\n")
        if not separator:
            raise GitOperationError(
                f"Annotated tag '{self.name}' has an invalid Git object format."
            )

        lines = header.splitlines()
        tag_headers = [
            index for index, line in enumerate(lines) if line.startswith("tag ")
        ]
        if len(tag_headers) != 1:
            raise GitOperationError(
                f"Annotated tag '{self.name}' does not contain one valid tag header."
            )

        lines[tag_headers[0]] = f"tag {destination}"
        return "\n".join(lines) + separator + message


@dataclass(frozen=True, slots=True)
class TagRefReplacement:
    """Prepared source-to-destination reference replacement."""

    source: str
    destination: str
    source_oid: str
    destination_oid: str

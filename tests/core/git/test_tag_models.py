# tests/core/git/test_tag_models.py

"""Tests for metadata-preserving Git tag models."""

import pytest

from app.core.git import TagSnapshot
from app.core.shared import GitOperationError


def _raw_tag(name: str, message: str = "Release notes\n") -> str:
    """Build one realistic unsigned annotated-tag object."""

    return (
        f"object {'a' * 40}\n"
        "type commit\n"
        f"tag {name}\n"
        "tagger Release Bot <release@example.com> 1700000000 +0700\n\n"
        f"{message}"
    )


def test_renamed_raw_object_changes_only_tag_header() -> None:
    """Preserve target, tagger identity/date/timezone, and message exactly."""

    source = _raw_tag("v1.2.3b1")
    snapshot = TagSnapshot(
        name="v1.2.3b1",
        ref_oid="b" * 40,
        object_type="tag",
        raw_object=source,
    )

    renamed = snapshot.renamed_raw_object("v1.2.3-beta.1")

    assert renamed == source.replace("tag v1.2.3b1", "tag v1.2.3-beta.1")
    assert "1700000000 +0700" in renamed
    assert renamed.endswith("Release notes\n")


@pytest.mark.parametrize("kind", ["PGP", "SSH"])
def test_signed_tag_is_detected_and_refused(kind: str) -> None:
    """Never preserve an invalid signature or silently strip it."""

    raw = _raw_tag(
        "v1.2.3b1",
        f"Release\n-----BEGIN {kind} SIGNATURE-----\ninvalid\n",
    )
    snapshot = TagSnapshot(
        name="v1.2.3b1",
        ref_oid="b" * 40,
        object_type="tag",
        raw_object=raw,
    )

    assert snapshot.is_signed is True
    with pytest.raises(GitOperationError, match="signed payload"):
        snapshot.renamed_raw_object("v1.2.3-beta.1")


def test_lightweight_tag_has_no_annotated_object() -> None:
    """Keep lightweight tags distinct from annotated tags."""

    snapshot = TagSnapshot(
        name="v1.2.3b1",
        ref_oid="a" * 40,
        object_type="commit",
    )

    assert snapshot.is_annotated is False
    with pytest.raises(GitOperationError, match="lightweight"):
        snapshot.renamed_raw_object("v1.2.3-beta.1")

# tests/core/reflow/test_tag_replacement.py

"""Tests for metadata-aware local and remote tag replacement."""

from unittest.mock import Mock, call

import pytest

from app.core.git import TagRefReplacement, TagSnapshot
from app.core.reflow import (
    PreparedTagReplacement,
    TagConversion,
    TagReplacementService,
)
from app.core.shared import GitOperationError


def _snapshot(*, annotated: bool = True, signed: bool = False) -> TagSnapshot:
    """Create one source snapshot used by replacement tests."""

    raw = None
    object_type = "commit"
    if annotated:
        object_type = "tag"
        raw = (
            f"object {'b' * 40}\n"
            "type commit\n"
            "tag v1.2.3b1\n"
            "tagger Test <test@example.com> 1700000000 +0000\n\n"
            "Release notes"
        )
        if signed:
            raw += "\n-----BEGIN PGP SIGNATURE-----\ninvalid\n"
    return TagSnapshot(
        name="v1.2.3b1",
        ref_oid="a" * 40,
        object_type=object_type,
        raw_object=raw,
    )


def _conversion() -> TagConversion:
    """Create the matching PEP 440-to-SemVer mapping."""

    return TagConversion(source="v1.2.3b1", destination="v1.2.3-beta.1")


def test_prepare_local_reads_metadata_without_mutating() -> None:
    """Keep planning read-only before confirmation and dry-run boundaries."""

    git = Mock()
    git.get_tag_snapshot.return_value = _snapshot()
    service = TagReplacementService(git)

    prepared = service.prepare((_conversion(),), remote=False)

    assert prepared[0].snapshot.ref_oid == "a" * 40
    git.create_replacement_ref.assert_not_called()
    git.replace_local_tags_atomically.assert_not_called()
    git.get_remote_tag_oid.assert_not_called()


def test_prepare_remote_verifies_source_and_absent_destination() -> None:
    """Snapshot exact remote state before constructing destination objects."""

    git = Mock()
    git.get_tag_snapshot.return_value = _snapshot()
    git.get_remote_tag_oid.side_effect = ["a" * 40, None]
    service = TagReplacementService(git)

    service.prepare((_conversion(),), remote=True)

    assert git.get_remote_tag_oid.call_args_list == [
        call("v1.2.3b1"),
        call("v1.2.3-beta.1"),
    ]


def test_prepare_remote_refuses_existing_destination() -> None:
    """Never resolve a remote collision by deleting the source automatically."""

    git = Mock()
    git.get_tag_snapshot.return_value = _snapshot()
    git.get_remote_tag_oid.side_effect = ["a" * 40, "c" * 40]

    with pytest.raises(GitOperationError, match="destination tag already exists"):
        TagReplacementService(git).prepare((_conversion(),), remote=True)


def test_prepare_refuses_signed_tag() -> None:
    """Stop before mutation when a source signature would become invalid."""

    git = Mock()
    git.get_tag_snapshot.return_value = _snapshot(signed=True)

    with pytest.raises(GitOperationError, match="cannot rename"):
        TagReplacementService(git).prepare((_conversion(),), remote=False)


@pytest.mark.parametrize("scope", ["local", "remote"])
def test_apply_materializes_then_uses_one_atomic_boundary(scope: str) -> None:
    """Create objects first and then invoke only the selected atomic operation."""

    git = Mock()
    snapshot = _snapshot()
    replacement = TagRefReplacement(
        source="v1.2.3b1",
        destination="v1.2.3-beta.1",
        source_oid="a" * 40,
        destination_oid="c" * 40,
    )
    git.create_replacement_ref.return_value = replacement
    service = TagReplacementService(git)
    item = PreparedTagReplacement(conversion=_conversion(), snapshot=snapshot)

    if scope == "local":
        result = service.replace_local((item,))
        git.replace_local_tags_atomically.assert_called_once_with([replacement])
        git.replace_remote_tags_atomically.assert_not_called()
    else:
        result = service.replace_remote((item,))
        git.replace_remote_tags_atomically.assert_called_once_with([replacement])
        git.replace_local_tags_atomically.assert_not_called()

    assert result == [replacement]

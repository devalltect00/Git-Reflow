# tests/core/reflow/test_tag_converter.py

"""
Tests for TagConverter.
"""

import pytest

from app.core.reflow import TagConverter, TagFormat


class TestTagConverter:
    """
    Tests for TagConverter.
    """

    @pytest.fixture
    def converter(
        self,
    ):
        """
        Create TagConverter.
        """
        return TagConverter()

    # =====================================================
    # pep440_to_semver_tag
    # =====================================================

    def test_convert_alpha_tag(
        self,
        converter,
    ):
        """
        Should convert alpha tags.
        """
        assert (
            converter.pep440_to_semver_tag(
                "v1.0.0a1",
            )
            == "v1.0.0-alpha.1"
        )

    def test_convert_beta_tag(
        self,
        converter,
    ):
        """
        Should convert beta tags.
        """
        assert (
            converter.pep440_to_semver_tag(
                "v1.0.0b1",
            )
            == "v1.0.0-beta.1"
        )

    def test_convert_rc_tag(
        self,
        converter,
    ):
        """
        Should convert rc tags.
        """
        assert (
            converter.pep440_to_semver_tag(
                "v1.0.0rc1",
            )
            == "v1.0.0-rc.1"
        )

    def test_keep_release_tag(
        self,
        converter,
    ):
        """
        Should keep stable tags unchanged.
        """
        assert (
            converter.pep440_to_semver_tag(
                "v1.0.0",
            )
            == "v1.0.0"
        )


class TestTagFormat:
    """Tests for destination-format normalization."""

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("semver", TagFormat.SEMVER),
            ("Semantic-Versioning", TagFormat.SEMVER),
            ("pep440", TagFormat.PEP440),
            ("PEP-440", TagFormat.PEP440),
            ("pep_440", TagFormat.PEP440),
            (TagFormat.PEP440, TagFormat.PEP440),
        ],
    )
    def test_from_value_accepts_supported_names(self, value, expected) -> None:
        """Normalize supported enum values and aliases."""

        assert TagFormat.from_value(value) is expected

    def test_from_value_rejects_unsupported_name(self) -> None:
        """Reject arbitrary formatting names with actionable choices."""

        with pytest.raises(ValueError, match="semver, pep440"):
            TagFormat.from_value("calendar-versioning")


class TestBidirectionalTagNames:
    """Tests for safe conversion in both supported directions."""

    @pytest.fixture
    def converter(self) -> TagConverter:
        """Create a converter whose name-only operations need no Git calls."""

        return TagConverter()

    @pytest.mark.parametrize(
        ("source", "expected"),
        [
            ("v1.2.3", "v1.2.3"),
            ("v1.2.3a1", "v1.2.3-alpha.1"),
            ("v1.2.3b2", "v1.2.3-beta.2"),
            ("v1.2.3rc3", "v1.2.3-rc.3"),
            ("v1.2.3.dev4", "v1.2.3-dev.4"),
            ("v1.2.3.post5", "v1.2.3+post.5"),
            ("v1.2.3+linux_x86", "v1.2.3+linux.x86"),
            ("v1.2.3.post5+linux_x86", "v1.2.3+post.5.linux.x86"),
            ("v01.002.0003b04", "v1.2.3-beta.4"),
        ],
    )
    def test_pep440_to_semver(self, converter, source, expected) -> None:
        """Convert supported PEP 440 phases without raw string replacement."""

        assert converter.pep440_to_semver_tag(source) == expected

    @pytest.mark.parametrize(
        ("source", "expected"),
        [
            ("v1.2.3", "v1.2.3"),
            ("v1.2.3-alpha.1", "v1.2.3a1"),
            ("v1.2.3-beta.2", "v1.2.3b2"),
            ("v1.2.3-rc.3", "v1.2.3rc3"),
            ("v1.2.3-dev.4", "v1.2.3.dev4"),
            ("v1.2.3+post.5", "v1.2.3.post5"),
            ("v1.2.3+linux.X86", "v1.2.3+linux.x86"),
            ("v1.2.3+post.5.linux.X86", "v1.2.3.post5+linux.x86"),
            ("1.2.3-beta.0+build-7", "1.2.3b0+build.7"),
        ],
    )
    def test_semver_to_pep440(self, converter, source, expected) -> None:
        """Convert supported SemVer phases and build metadata into PEP 440."""

        assert converter.semver_to_pep440_tag(source) == expected

    @pytest.mark.parametrize(
        "source",
        [
            "release-1.2.3",
            "v1.2",
            "v1.2.3rc1.dev2",
            "v1.2.3.post1.dev2",
        ],
    )
    def test_pep440_conversion_rejects_unsafe_input(
        self,
        converter,
        source,
    ) -> None:
        """Reject non-version tags and lossy compound PEP 440 phases."""

        with pytest.raises(ValueError):
            converter.pep440_to_semver_tag(source)

    @pytest.mark.parametrize(
        "source",
        [
            "v1.2.3-preview.1",
            "v1.2.3-alpha.1+post.2",
            "v01.2.3-alpha.1",
        ],
    )
    def test_semver_conversion_rejects_unsafe_input(
        self,
        converter,
        source,
    ) -> None:
        """Reject SemVer tags with no safe PEP 440 representation."""

        with pytest.raises(ValueError):
            converter.semver_to_pep440_tag(source)

    def test_convert_tag_name_is_idempotent_for_target_format(
        self,
        converter,
    ) -> None:
        """Never rewrite an already-conforming SemVer prerelease tag."""

        source = "v1.2.3-beta.1"

        assert converter.convert_tag_name(source, TagFormat.SEMVER) == source

    def test_convert_tag_name_keeps_existing_pep440_tag(self, converter) -> None:
        """Keep an already-conforming PEP 440 tag unchanged."""

        source = "v1.2.3b1"

        assert converter.convert_tag_name(source, TagFormat.PEP440) == source


class TestTagConversionPlanning:
    """Tests for collision and unsupported-tag handling before mutation."""

    @pytest.fixture
    def converter(self) -> TagConverter:
        """Create a converter backed by a mutation-observable Git mock."""

        return TagConverter()

    def test_reported_mixed_tags_plan_zero_mutations(self, converter) -> None:
        """Skip the exact collision set from the reported production failure."""

        tags = [
            "v1.2.3b1",
            "v1.2.3b2",
            "v1.2.3-beta.1",
            "v1.2.3-beta.2",
        ]

        plan = converter.plan_conversions(tags)

        assert plan.conversions == ()
        assert len(plan.skipped) == 4
        assert "destination tag already exists" in plan.skipped[0].reason
        assert "destination tag already exists" in plan.skipped[1].reason
        assert plan.skipped[2].reason == "already matches semver"
        assert plan.skipped[3].reason == "already matches semver"

    def test_plan_reserves_new_destination_against_duplicate_alias(
        self, converter
    ) -> None:
        """Allow only the first source tag when aliases share a destination."""

        plan = converter.plan_conversions(["v1.2.3b01", "v1.2.3b1"])

        assert [(item.source, item.destination) for item in plan.conversions] == [
            ("v1.2.3b01", "v1.2.3-beta.1")
        ]
        assert plan.skipped[0].tag == "v1.2.3b1"
        assert "destination tag already exists" in plan.skipped[0].reason

    def test_plan_skips_unsupported_tag_with_reason(self, converter) -> None:
        """Keep unrelated Git tags out of the mutation plan."""

        plan = converter.plan_conversions(["nightly", "v2.0.0rc1"])

        assert plan.conversions[0].destination == "v2.0.0-rc.1"
        assert plan.skipped[0].tag == "nightly"
        assert "not a supported PEP 440 tag" in plan.skipped[0].reason

    def test_plan_converts_semver_to_pep440(self, converter) -> None:
        """Plan the reverse direction when PEP 440 is selected."""

        plan = converter.plan_conversions(
            ["v2.0.0-beta.3"],
            TagFormat.PEP440,
        )

        assert plan.target_format is TagFormat.PEP440
        assert plan.conversions[0].destination == "v2.0.0b3"

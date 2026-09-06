# tests/core/reflow/test_tag_processor.py

"""
Tests for TagProcessor.

This module tests tag validation and filtering logic.
"""

from app.core.reflow import TagProcessor


class TestTagProcessor:
    """
    Tests for TagProcessor.
    """

    # =====================================================
    # is_valid
    # =====================================================

    def test_is_valid_returns_true_for_stable_tag(self):
        """
        Should return True for a stable version tag.
        """
        processor = TagProcessor()

        assert processor.is_valid("v1.0.0") is True

    def test_is_valid_returns_true_for_rc_tag(self):
        """
        Should return True for a release candidate tag.
        """
        processor = TagProcessor()

        assert processor.is_valid("v1.0.0-rc1") is True

    def test_is_valid_returns_true_for_beta_tag(self):
        """
        Should return True for a beta tag.
        """
        processor = TagProcessor()

        assert processor.is_valid("v1.0.0-beta.1") is True

    def test_is_valid_returns_true_for_alpha_tag(self):
        """
        Should return True for an alpha tag.
        """
        processor = TagProcessor()

        assert processor.is_valid("v1.0.0-alpha.1") is True

    def test_is_valid_returns_false_without_v_prefix(self):
        """
        Should return False when the tag does not start with 'v'.
        """
        processor = TagProcessor()

        assert processor.is_valid("1.0.0") is False

    def test_is_valid_returns_false_for_random_text(self):
        """
        Should return False for an invalid tag.
        """
        processor = TagProcessor()

        assert processor.is_valid("hello-world") is False

    def test_is_valid_returns_false_for_empty_string(self):
        """
        Should return False for an empty string.
        """
        processor = TagProcessor()

        assert processor.is_valid("") is False

    # =====================================================
    # is_stable
    # =====================================================

    def test_is_stable_returns_true_for_release_tag(self):
        """
        Should return True for a stable release tag.
        """
        processor = TagProcessor()

        assert processor.is_stable("v1.0.0") is True

    def test_is_stable_returns_false_for_rc_tag(self):
        """
        Should return False for a release candidate tag.
        """
        processor = TagProcessor()

        assert processor.is_stable("v1.0.0-rc1") is False

    def test_is_stable_returns_false_for_beta_tag(self):
        """
        Should return False for a beta tag.
        """
        processor = TagProcessor()

        assert processor.is_stable("v1.0.0-beta.1") is False

    def test_is_stable_returns_false_for_alpha_tag(self):
        """
        Should return False for an alpha tag.
        """
        processor = TagProcessor()

        assert processor.is_stable("v1.0.0-alpha.1") is False

    # =====================================================
    # filter_valid_tags
    # =====================================================

    def test_filter_valid_tags_returns_only_valid_tags(self):
        """
        Should return only valid tags.
        """
        processor = TagProcessor()

        tags = [
            "v1.0.0",
            "v1.1.0",
            "invalid",
            "hello",
            "v2.0.0-rc1",
        ]

        result = processor.filter_valid_tags(tags)

        assert result == [
            "v1.0.0",
            "v1.1.0",
            "v2.0.0-rc1",
        ]

    def test_filter_valid_tags_returns_empty_list(self):
        """
        Should return an empty list when all tags are invalid.
        """
        processor = TagProcessor()

        tags = [
            "invalid",
            "hello",
            "1.0.0",
        ]

        result = processor.filter_valid_tags(tags)

        assert result == []

    # =====================================================
    # filter_stable_tags
    # =====================================================

    def test_filter_stable_tags_returns_only_stable_tags(self):
        """
        Should return only stable tags.
        """
        processor = TagProcessor()

        tags = [
            "v1.0.0",
            "v1.1.0",
            "v2.0.0-rc1",
            "v2.0.0-beta.1",
        ]

        result = processor.filter_stable_tags(tags)

        assert result == [
            "v1.0.0",
            "v1.1.0",
        ]

    def test_filter_stable_tags_returns_empty_list(self):
        """
        Should return an empty list when no stable tags exist.
        """
        processor = TagProcessor()

        tags = [
            "v1.0.0-rc1",
            "v1.0.0-beta.1",
        ]

        result = processor.filter_stable_tags(tags)

        assert result == []

    # =====================================================
    # filter_valid_stable_tags
    # =====================================================

    def test_filter_valid_stable_tags_returns_only_valid_stable_tags(self):
        """
        Should return only tags that are both valid and stable.
        """
        processor = TagProcessor()

        tags = [
            "v1.0.0",
            "v1.1.0",
            "v2.0.0-rc1",
            "invalid",
            "hello",
        ]

        result = processor.filter_valid_stable_tags(tags)

        assert result == [
            "v1.0.0",
            "v1.1.0",
        ]

    def test_filter_valid_stable_tags_returns_empty_list(self):
        """
        Should return an empty list when no valid stable tags exist.
        """
        processor = TagProcessor()

        tags = [
            "invalid",
            "hello",
            "v2.0.0-rc1",
            "v2.0.0-beta.1",
        ]

        result = processor.filter_valid_stable_tags(tags)

        assert result == []

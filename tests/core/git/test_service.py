# tests/core/git/test_service.py

"""
Tests for GitService.

This module tests Git business logic.
"""

from unittest.mock import Mock, patch

import pytest

from app.core.git.service import GitService
from app.core.shared import GitOperationError


class TestGitService:
    """
    Tests for GitService.
    """

    @pytest.fixture
    def executor(self):
        """
        Create a mock Git executor.
        """
        return Mock()

    @pytest.fixture
    def service(
        self,
        executor,
        mock_config,
    ):
        """
        Create GitService instance.
        """
        return GitService(
            executor=executor,
            config=mock_config,
        )

    # =====================================================
    # Repository
    # =====================================================

    def test_is_git_repo_returns_true(
        self,
        service,
        executor,
    ):
        executor.rev_parse_inside_work_tree.return_value.success = True

        assert service.is_git_repo() is True

    def test_is_git_repo_returns_false(
        self,
        service,
        executor,
    ):
        with patch(
            "pathlib.Path.exists",
            return_value=False,
        ):
            executor.rev_parse_inside_work_tree.return_value.success = False

            assert service.is_git_repo() is False

    # =====================================================
    # Remote
    # =====================================================

    def test_get_remote_url_returns_url(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should return remote URL.
        """
        success_result.stdout = "https://github.com/example/repo.git\n"

        executor.remote_get_url.return_value = success_result

        result = service.get_remote_url()

        assert result == "https://github.com/example/repo.git"

    def test_get_remote_url_returns_none(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should return None when remote is unavailable.
        """
        executor.remote_get_url.return_value = failed_result

        assert service.get_remote_url() is None

    def test_remote_exists_returns_true(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should return True when remote exists.
        """
        executor.remote_get_url.return_value = success_result

        assert service.remote_exists() is True

    def test_remote_exists_returns_false(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should return False when remote does not exist.
        """
        executor.remote_get_url.return_value = failed_result

        assert service.remote_exists() is False

    # =====================================================
    # Tags
    # =====================================================

    def test_get_all_tags_returns_tags(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should return parsed tags.
        """
        success_result.stdout = "v1.0.0\nv1.1.0\nv2.0.0"

        executor.get_all_tags.return_value = success_result

        result = service.get_all_tags()

        assert result == [
            "v1.0.0",
            "v1.1.0",
            "v2.0.0",
        ]

    def test_get_all_tags_raises_on_failure(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should distinguish command failure from a repository with no tags.
        """
        executor.get_all_tags.return_value = failed_result

        with pytest.raises(GitOperationError, match="Failed to retrieve Git tags"):
            service.get_all_tags()

    def test_get_all_tags_returns_empty_list_for_empty_output(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should return empty list when output is empty.
        """
        success_result.stdout = ""

        executor.get_all_tags.return_value = success_result

        result = service.get_all_tags()

        assert result == []

    def test_get_tag_commit_sha_returns_sha(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should return commit SHA.
        """
        success_result.stdout = "abc123\n"

        executor.get_tag_commit_sha.return_value = success_result

        result = service.get_tag_commit_sha(
            "v1.0.0",
        )

        assert result == "abc123"

    def test_get_tag_commit_sha_returns_none(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should return None on failure.
        """
        executor.get_tag_commit_sha.return_value = failed_result

        result = service.get_tag_commit_sha(
            "v1.0.0",
        )

        assert result is None

    def test_get_tag_message_returns_message(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should return tag message.
        """
        success_result.stdout = "Release notes"

        executor.get_tag_message.return_value = success_result

        result = service.get_tag_message(
            "v1.0.0",
        )

        assert result == "Release notes"

    def test_get_tag_message_returns_empty_string(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should return empty string on failure.
        """
        executor.get_tag_message.return_value = failed_result

        result = service.get_tag_message(
            "v1.0.0",
        )

        assert result == ""

    def test_create_annotated_tag_success(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should create annotated tag.
        """
        executor.create_annotated_tag.return_value = success_result

        service.create_annotated_tag(
            "v2.0.0",
            "abc123",
            "msg.txt",
        )

        executor.create_annotated_tag.assert_called_once()

    def test_create_annotated_tag_raises_git_operation_error(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should raise GitOperationError on failure.
        """
        executor.create_annotated_tag.return_value = failed_result

        with pytest.raises(
            GitOperationError,
        ):
            service.create_annotated_tag(
                "v2.0.0",
                "abc123",
                "msg.txt",
            )

    def test_delete_local_tag_success(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should delete local tag.
        """
        executor.delete_local_tag.return_value = success_result

        service.delete_local_tag(
            "v1.0.0",
        )

        executor.delete_local_tag.assert_called_once()

    def test_delete_local_tag_raises_git_operation_error(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should raise GitOperationError on failure.
        """
        executor.delete_local_tag.return_value = failed_result

        with pytest.raises(
            GitOperationError,
        ):
            service.delete_local_tag(
                "v1.0.0",
            )

    # =====================================================
    # Push Tag
    # =====================================================

    def test_push_tag_success(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should push tag successfully.
        """
        executor.push_tag.return_value = success_result

        service.push_tag("v1.0.0")

        executor.push_tag.assert_called_once()

    def test_push_tag_raises_git_operation_error(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should raise GitOperationError on failure.
        """
        executor.push_tag.return_value = failed_result

        with pytest.raises(
            GitOperationError,
        ):
            service.push_tag("v1.0.0")

    # =====================================================
    # Delete Tag
    # =====================================================

    def test_delete_remote_tag_success(
        self,
        service,
        executor,
        success_result,
    ):
        """
        Should delete remote tag successfully.
        """
        executor.delete_remote_tag.return_value = success_result

        service.delete_remote_tag("v1.0.0")

        executor.delete_remote_tag.assert_called_once()

    def test_delete_remote_tag_raises_git_operation_error(
        self,
        service,
        executor,
        failed_result,
    ):
        """
        Should raise GitOperationError on failure.
        """
        executor.delete_remote_tag.return_value = failed_result

        with pytest.raises(
            GitOperationError,
        ):
            service.delete_remote_tag("v1.0.0")

    def test_tag_worktree_yields_and_removes_checkout(
        self,
        service,
        executor,
        success_result,
    ):
        """Materialize a tag and always remove its detached worktree."""
        executor.add_detached_worktree.return_value = success_result
        executor.remove_worktree.return_value = success_result

        with service.tag_worktree("v1.0.0") as worktree:
            assert worktree.name == "checkout"
            executor.add_detached_worktree.assert_called_once_with(
                tag="v1.0.0",
                path=worktree,
            )

        executor.remove_worktree.assert_called_once_with(worktree)

    def test_tag_worktree_raises_when_creation_fails(
        self,
        service,
        executor,
        failed_result,
    ):
        """Stop before a Docker build when the tag cannot be materialized."""
        executor.add_detached_worktree.return_value = failed_result

        with pytest.raises(GitOperationError, match="temporary worktree"):
            with service.tag_worktree("v1.0.0"):
                pytest.fail("failed worktree must not yield")

        executor.remove_worktree.assert_not_called()

    def test_tag_worktree_logs_failed_cleanup(
        self,
        service,
        executor,
        success_result,
        failed_result,
        caplog,
    ):
        """Report cleanup failure without hiding successful work."""
        executor.add_detached_worktree.return_value = success_result
        executor.remove_worktree.return_value = failed_result

        with service.tag_worktree("v1.0.0"):
            pass

        assert "Failed to remove temporary worktree" in caplog.text

    # =====================================================
    # Dry Run
    # =====================================================

    def test_get_is_dry_run(
        self,
        service,
        executor,
    ):
        """
        Should return executor dry-run state.
        """
        executor.get_is_dry_run.return_value = True

        assert service.get_is_dry_run() is True

    def test_set_is_dry_run(
        self,
        service,
        executor,
    ):
        """
        Should delegate dry-run state.
        """
        service.set_is_dry_run(True)

        executor.set_is_dry_run.assert_called_once_with(True)

    # =====================================================
    # Silent
    # =====================================================

    def test_get_silent(
        self,
        service,
        executor,
    ):
        """
        Should return executor silent state.
        """
        executor.get_silent.return_value = True

        assert service.get_silent() is True

    def test_set_silent(
        self,
        service,
        executor,
    ):
        """
        Should delegate silent state.
        """
        service.set_silent(True)

        executor.set_silent.assert_called_once_with(True)

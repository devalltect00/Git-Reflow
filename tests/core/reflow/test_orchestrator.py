# tests/core/reflow/test_orchestrator.py

"""
Tests for Orchestrator.

This module tests the Reflow workflow orchestration layer.
"""

from unittest.mock import Mock, patch

import pytest

from app.core.reflow.orchestrator import Orchestrator
from app.core.shared import GitOperationError


class TestOrchestrator:
    """
    Tests for Orchestrator.
    """

    @pytest.fixture
    def mock_git(self):
        """
        Create mock Git service.
        """
        return Mock()

    @pytest.fixture
    def mock_github(self):
        """
        Create mock GitHub service.
        """
        return Mock()

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    def test_init_creates_services(
        self,
        mock_create_github_service,
        mock_create_git_service,
        mock_git,
        mock_github,
    ):
        """
        Should create Git and GitHub services.
        """
        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github

        orchestrator = Orchestrator()

        assert orchestrator.git is mock_git
        assert orchestrator.github is mock_github

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    def test_init_passes_repository_to_services(
        self,
        mock_create_github_service,
        mock_create_git_service,
        tmp_path,
    ):
        """Wire the same explicit target into Git and GitHub services."""
        Orchestrator(repository=tmp_path)

        mock_create_git_service.assert_called_once_with(
            dry_run=False,
            is_silent=False,
            repository=tmp_path,
        )
        mock_create_github_service.assert_called_once_with(
            dry_run=False,
            is_silent=False,
            repository=tmp_path,
        )

    # =====================================================
    # _process_tag
    # =====================================================

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    @patch("app.core.reflow.orchestrator.time.sleep")
    def test_process_tag_skips_existing_release(
        self,
        mock_sleep,
        mock_create_github_service,
        mock_create_git_service,
        mock_git,
        mock_github,
    ):
        """
        Should skip tags that already have releases.
        """
        mock_github.release_exists.return_value = True

        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github

        orchestrator = Orchestrator()

        orchestrator._process_tag("v1.0.0")

        mock_git.delete_remote_tag.assert_not_called()
        mock_git.push_tag.assert_not_called()

        mock_sleep.assert_not_called()

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    @patch("app.core.reflow.orchestrator.time.sleep")
    def test_process_tag_repushes_missing_release(
        self,
        mock_sleep,
        mock_create_github_service,
        mock_create_git_service,
        mock_git,
        mock_github,
    ):
        """
        Should re-push tags without releases.
        """
        mock_github.release_exists.return_value = False

        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github

        orchestrator = Orchestrator()

        orchestrator._process_tag("v1.0.0")

        mock_git.delete_remote_tag.assert_called_once_with("v1.0.0")

        mock_git.push_tag.assert_called_once_with("v1.0.0")

        mock_sleep.assert_called_once()

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    @patch("app.core.reflow.orchestrator.time.sleep")
    def test_process_tag_dry_run_does_not_sleep(
        self,
        mock_sleep,
        mock_create_github_service,
        mock_create_git_service,
        mock_git,
        mock_github,
    ):
        """Avoid artificial delays while previewing release recovery."""
        mock_github.release_exists.return_value = False
        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github
        orchestrator = Orchestrator(dry_run=True)

        orchestrator._process_tag("v1.0.0")

        mock_git.delete_remote_tag.assert_called_once_with("v1.0.0")
        mock_git.push_tag.assert_called_once_with("v1.0.0")
        mock_sleep.assert_not_called()

    # =====================================================
    # run
    # =====================================================

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    def test_run_returns_when_not_git_repo(
        self,
        mock_create_github_service,
        mock_create_git_service,
        mock_git,
        mock_github,
    ):
        """
        Should stop when current directory is not a Git repository.
        """
        mock_git.is_git_repo.return_value = False

        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github

        orchestrator = Orchestrator()

        orchestrator.run()

        mock_git.get_all_tags.assert_not_called()

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    @patch.object(
        Orchestrator,
        "_process_tag",
    )
    def test_run_processes_valid_tags(
        self,
        mock_process_tag,
        mock_create_github_service,
        mock_create_git_service,
        mock_git,
        mock_github,
    ):
        """
        Should process valid tags.
        """
        mock_git.is_git_repo.return_value = True

        mock_git.get_all_tags.return_value = [
            "v1.0.0",
            "v1.1.0",
        ]

        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github

        orchestrator = Orchestrator()

        orchestrator.run()

        assert mock_process_tag.call_count == 2

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    @patch.object(
        Orchestrator,
        "_process_tag",
    )
    def test_run_applies_limit(
        self,
        mock_process_tag,
        mock_create_github_service,
        mock_create_git_service,
        mock_git,
        mock_github,
    ):
        """
        Should respect the limit option.
        """
        mock_git.is_git_repo.return_value = True

        mock_git.get_all_tags.return_value = [
            "v1.0.0",
            "v1.1.0",
            "v1.2.0",
        ]

        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github

        orchestrator = Orchestrator()

        orchestrator.run(
            limit=1,
        )

        assert mock_process_tag.call_count == 1

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    @patch.object(
        Orchestrator,
        "_process_tag",
    )
    def test_run_processes_only_stable_tags(
        self,
        mock_process_tag,
        mock_create_github_service,
        mock_create_git_service,
        mock_git,
        mock_github,
    ):
        """
        Should process only stable tags when requested.
        """
        mock_git.is_git_repo.return_value = True

        mock_git.get_all_tags.return_value = [
            "v1.0.0",
            "v1.1.0-rc1",
            "v1.2.0",
        ]

        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github

        orchestrator = Orchestrator()

        orchestrator.run(
            only_stable=True,
        )

        processed_tags = [call.args[0] for call in mock_process_tag.call_args_list]

        assert processed_tags == [
            "v1.0.0",
            "v1.2.0",
        ]

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    @patch.object(
        Orchestrator,
        "_process_tag",
    )
    def test_run_continues_after_processing_error(
        self,
        mock_process_tag,
        mock_create_github_service,
        mock_create_git_service,
        mock_git,
        mock_github,
    ):
        """
        Should continue processing remaining tags
        after an error.
        """
        mock_git.is_git_repo.return_value = True

        mock_git.get_all_tags.return_value = [
            "v1.0.0",
            "v1.1.0",
        ]

        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github

        mock_process_tag.side_effect = [
            GitOperationError("failure"),
            None,
        ]

        orchestrator = Orchestrator()

        orchestrator.run()

        assert mock_process_tag.call_count == 2

    @patch("app.core.reflow.orchestrator.console.print")
    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    @patch.object(
        Orchestrator,
        "_process_tag",
    )
    def test_run_prints_failed_tags(
        self,
        mock_process_tag,
        mock_create_github_service,
        mock_create_git_service,
        mock_console,
        mock_git,
        mock_github,
    ):
        """
        Should print failed tags summary.
        """
        mock_git.is_git_repo.return_value = True

        mock_git.get_all_tags.return_value = [
            "v1.0.0",
        ]

        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github

        mock_process_tag.side_effect = GitOperationError("boom")

        orchestrator = Orchestrator()

        orchestrator.run()

        printed_messages = [
            call.args[0]
            for call in mock_console.call_args_list
            if call.args and isinstance(call.args[0], str)
        ]

        assert any("Failed tags" in message for message in printed_messages)

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    @patch.object(Orchestrator, "_process_tag")
    def test_run_propagates_unexpected_processing_error(
        self,
        mock_process_tag,
        mock_create_github_service,
        mock_create_git_service,
        mock_git,
        mock_github,
    ):
        """Let the CLI boundary report unexpected programming failures."""
        mock_git.is_git_repo.return_value = True
        mock_git.get_all_tags.return_value = ["v1.0.0"]
        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github
        mock_process_tag.side_effect = RuntimeError("unexpected")

        with pytest.raises(RuntimeError, match="unexpected"):
            Orchestrator().run()

    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    def test_run_returns_when_no_valid_tags(
        self,
        mock_create_github_service,
        mock_create_git_service,
        mock_git,
        mock_github,
    ):
        """
        Should stop when no valid tags exist.
        """
        mock_git.is_git_repo.return_value = True

        mock_git.get_all_tags.return_value = [
            "invalid-tag",
        ]

        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github

        orchestrator = Orchestrator()

        orchestrator.run()

    @patch("app.core.reflow.orchestrator.console.print")
    @patch("app.core.reflow.orchestrator.create_git_service")
    @patch("app.core.reflow.orchestrator.create_github_service")
    @patch.object(Orchestrator, "_process_tag")
    def test_run_reports_dry_run_completion_without_remote_changes(
        self,
        mock_process_tag,
        mock_create_github_service,
        mock_create_git_service,
        mock_console,
        mock_git,
        mock_github,
    ):
        """Describe successful release recovery as a non-mutating preview."""
        mock_git.is_git_repo.return_value = True
        mock_git.get_all_tags.return_value = ["v1.0.0"]
        mock_create_git_service.return_value = mock_git
        mock_create_github_service.return_value = mock_github

        Orchestrator(dry_run=True).run()

        mock_process_tag.assert_called_once_with("v1.0.0")
        printed_messages = [
            call.args[0]
            for call in mock_console.call_args_list
            if call.args and isinstance(call.args[0], str)
        ]
        assert any(
            "release recovery preview" in message for message in printed_messages
        )
        assert any(
            "No remote tags were deleted or pushed" in message
            for message in printed_messages
        )

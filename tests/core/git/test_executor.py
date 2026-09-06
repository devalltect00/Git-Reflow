# tests/core/git/test_executor.py

"""
Tests for GitExecutor.

This module tests Git command execution.
"""

from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import Mock

from app.core.git.executor import GitExecutor


class TestGitExecutor:
    """
    Tests for GitExecutor.
    """

    # =====================================================
    # _run
    # =====================================================

    def test_run_returns_command_result(self):
        """
        Should convert CompletedProcess into CommandResult.
        """
        executor = GitExecutor()

        executor.runner = Mock()

        executor.runner.run.return_value = CompletedProcess(
            args=["git", "--version"],
            returncode=0,
            stdout="git version",
            stderr="",
        )

        result = executor._run(["--version"])

        assert result.success is True
        assert result.stdout == "git version"
        assert result.stderr == ""
        assert executor.runner.run.call_args.kwargs["cwd"] == Path.cwd()

    def test_run_uses_selected_repository(self, tmp_path):
        """Execute Git commands from the explicit repository target."""
        executor = GitExecutor(repository=tmp_path)
        executor.runner = Mock()
        executor.runner.run.return_value = CompletedProcess(
            args=["git", "status"],
            returncode=0,
            stdout="",
            stderr="",
        )

        executor._run(["status"], mutates=False)

        assert executor.runner.run.call_args.kwargs["cwd"] == tmp_path.resolve()

    def test_run_returns_dry_run_result(self):
        """
        Should return dry-run result when Runner
        returns None.
        """
        executor = GitExecutor()

        executor.runner = Mock()

        executor.runner.run.return_value = None

        result = executor._run(["tag"])

        assert result.success is True
        assert result.skipped is True

    # =====================================================
    # Repository
    # =====================================================

    def test_rev_parse_inside_work_tree(self):
        """
        Should execute repository validation command.
        """
        executor = GitExecutor()

        executor._run = Mock()

        executor.rev_parse_inside_work_tree()

        executor._run.assert_called_once_with(
            [
                "rev-parse",
                "--is-inside-work-tree",
            ],
            check=False,
            mutates=False,
        )

    def test_get_all_tags(self):
        """
        Should execute tag listing command.
        """
        executor = GitExecutor()

        executor._run = Mock()

        executor.get_all_tags()

        executor._run.assert_called_once_with(
            [
                "tag",
                "--sort=creatordate",
            ],
            check=True,
            mutates=False,
        )

    def test_get_tag_commit_sha(self):
        """
        Should execute SHA lookup command.
        """
        executor = GitExecutor()

        executor._run = Mock()

        executor.get_tag_commit_sha(
            "v1.0.0",
        )

        executor._run.assert_called_once_with(
            [
                "rev-list",
                "-n",
                "1",
                "v1.0.0",
            ],
            check=True,
            mutates=False,
        )

    def test_get_tag_message(self):
        """
        Should execute tag message command.
        """
        executor = GitExecutor()

        executor._run = Mock()

        executor.get_tag_message(
            "v1.0.0",
        )

        executor._run.assert_called_once_with(
            [
                "tag",
                "-l",
                "--format=%(contents)",
                "v1.0.0",
            ],
            check=True,
            mutates=False,
        )

    def test_create_annotated_tag(self):
        """
        Should execute annotated tag creation.
        """
        executor = GitExecutor()

        executor._run = Mock()

        executor.create_annotated_tag(
            "v2.0.0",
            "abc123",
            "message.txt",
        )

        executor._run.assert_called_once_with(
            [
                "tag",
                "-a",
                "v2.0.0",
                "abc123",
                "-F",
                "message.txt",
            ],
            check=True,
        )

    # =====================================================
    # Tags
    # =====================================================

    def test_push_tag(self):
        """
        Should execute push tag command.
        """
        executor = GitExecutor()

        executor._run = Mock()

        executor.push_tag(
            "origin",
            "v1.0.0",
        )

        executor._run.assert_called_once_with(
            [
                "push",
                "origin",
                "v1.0.0",
            ],
            check=True,
        )

    def test_delete_remote_tag(self):
        """
        Should execute delete tag command.
        """
        executor = GitExecutor()

        executor._run = Mock()

        executor.delete_remote_tag(
            "origin",
            "v1.0.0",
        )

        executor._run.assert_called_once_with(
            [
                "push",
                "origin",
                "--delete",
                "v1.0.0",
            ],
            check=False,
        )

    def test_worktree_commands(self, tmp_path):
        """Add and remove detached worktrees with the requested target path."""
        executor = GitExecutor()
        executor._run = Mock()

        executor.add_detached_worktree("v1.0.0", tmp_path)
        executor.remove_worktree(tmp_path)

        assert executor._run.call_args_list[0].args[0] == [
            "worktree",
            "add",
            "--detach",
            str(tmp_path),
            "v1.0.0",
        ]
        assert executor._run.call_args_list[1].args[0] == [
            "worktree",
            "remove",
            "--force",
            str(tmp_path),
        ]

    def test_delete_local_tag(self):
        """
        Should execute local tag deletion.
        """
        executor = GitExecutor()

        executor._run = Mock()

        executor.delete_local_tag(
            "v1.0.0",
        )

        executor._run.assert_called_once_with(
            [
                "tag",
                "-d",
                "v1.0.0",
            ],
            check=True,
        )

    # =====================================================
    # Remote
    # =====================================================

    def test_remote_get_url(self):
        """
        Should execute remote URL command.
        """
        executor = GitExecutor()

        executor._run = Mock()

        executor.remote_get_url(
            "origin",
        )

        executor._run.assert_called_once_with(
            [
                "remote",
                "get-url",
                "origin",
            ],
            check=False,
            mutates=False,
        )

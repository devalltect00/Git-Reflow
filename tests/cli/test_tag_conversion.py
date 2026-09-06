# tests/cli/test_tag_conversion.py

"""CLI and resolver tests for scoped, atomic tag replacement."""

from pathlib import Path
from unittest.mock import Mock

import pytest
from typer.testing import CliRunner

from app.cli.commands.reflow.common.models import ReflowExecutionArgs
from app.cli.commands.reflow.tags.convert.models import TagConversionScope
from app.cli.commands.reflow.tags.convert.resolver import resolve_convert_tags_args
from app.cli.constants.enums import LogLevelChoices
from app.cli.main import app
from app.core.git import TagSnapshot
from app.core.reflow import TagFormat
from app.core.repository import RepositoryTarget
from app.core.shared import ConfigurationError

runner = CliRunner()


def _snapshot(tag: str = "v1.2.3b1", *, signed: bool = False) -> TagSnapshot:
    """Create an annotated source snapshot for command tests."""

    signature = (
        "\n-----BEGIN PGP SIGNATURE-----\ninvalid-test-signature\n"
        "-----END PGP SIGNATURE-----\n"
        if signed
        else ""
    )
    return TagSnapshot(
        name=tag,
        ref_oid="a" * 40,
        object_type="tag",
        raw_object=(
            f"object {'b' * 40}\n"
            "type commit\n"
            f"tag {tag}\n"
            "tagger Test User <test@example.com> 1700000000 +0000\n\n"
            f"Release notes{signature}"
        ),
    )


def _install_git(
    monkeypatch,
    *,
    tags: list[str],
    signed: bool = False,
) -> Mock:
    """Install a metadata-aware Git service double."""

    git = Mock()
    git.is_git_repo.return_value = True
    git.get_all_tags.return_value = tags
    git.get_tag_snapshot.side_effect = lambda tag: _snapshot(tag, signed=signed)
    git.get_remote_tag_oid.side_effect = lambda tag: "a" * 40 if tag in tags else None
    monkeypatch.setattr(
        "app.cli.commands.reflow.tags.convert.command.create_git_service",
        Mock(return_value=git),
    )
    return git


def _command(tmp_path: Path, scope: str, *options: str) -> list[str]:
    """Create one local-target conversion command."""

    return [
        "--no-banner",
        "-C",
        str(tmp_path),
        "tags",
        "convert",
        scope,
        *options,
    ]


def test_convert_requires_explicit_scope(tmp_path: Path) -> None:
    """Do not infer local or remote persistence from legacy flags."""

    result = runner.invoke(
        app,
        ["--no-banner", "-C", str(tmp_path), "tags", "convert"],
    )

    assert result.exit_code != 0
    assert "local" in result.stdout
    assert "remote" in result.stdout


def test_local_conversion_decline_makes_no_changes(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Abort before destination objects or refs are created."""

    git = _install_git(monkeypatch, tags=["v1.2.3b1"])
    result = runner.invoke(app, _command(tmp_path, "local"), input="n\n")

    assert result.exit_code != 0
    assert "local tag replacement" in result.stdout
    assert "Apply this tag replacement plan?" in result.stdout
    git.create_replacement_ref.assert_not_called()
    git.replace_local_tags_atomically.assert_not_called()
    git.replace_remote_tags_atomically.assert_not_called()


def test_local_yes_applies_one_atomic_transaction(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Replace all approved local refs through the local service boundary."""

    git = _install_git(monkeypatch, tags=["v1.2.3rc1"])
    result = runner.invoke(app, _command(tmp_path, "local", "--yes"))

    assert result.exit_code == 0
    assert "Replaced 1 local tag(s) atomically" in result.stdout
    git.create_replacement_ref.assert_called_once()
    git.replace_local_tags_atomically.assert_called_once()
    git.replace_remote_tags_atomically.assert_not_called()


def test_remote_yes_applies_one_atomic_push(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Make remote replacement intrinsic rather than controlled by --push."""

    git = _install_git(monkeypatch, tags=["v1.2.3b1"])
    result = runner.invoke(app, _command(tmp_path, "remote", "-y"))

    assert result.exit_code == 0
    assert "guarded atomic remote push" in result.stdout
    assert "Replaced 1 remote tag(s) atomically" in result.stdout
    git.replace_remote_tags_atomically.assert_called_once()
    git.replace_local_tags_atomically.assert_not_called()


@pytest.mark.parametrize("scope", ["local", "remote"])
def test_dry_run_inspects_but_never_materializes_or_replaces_refs(
    monkeypatch,
    tmp_path: Path,
    scope: str,
) -> None:
    """Prove dry-run stops before every persistent tag mutation boundary."""

    git = _install_git(monkeypatch, tags=["v1.2.3b1"])
    confirm = Mock(side_effect=AssertionError("dry-run must not prompt"))
    monkeypatch.setattr(
        "app.cli.commands.reflow.tags.convert.command.typer.confirm",
        confirm,
    )

    command = _command(tmp_path, scope)
    command.insert(1, "--dry-run")
    result = runner.invoke(app, command)

    assert result.exit_code == 0
    assert "Would replace 1 tag(s)" in result.stdout
    assert "No tag objects, local refs, or remote refs were changed" in result.stdout
    git.get_tag_snapshot.assert_called_once()
    git.create_replacement_ref.assert_not_called()
    git.replace_local_tags_atomically.assert_not_called()
    git.replace_remote_tags_atomically.assert_not_called()
    confirm.assert_not_called()


def test_reverse_conversion_to_pep440(monkeypatch, tmp_path: Path) -> None:
    """Select SemVer-to-PEP-440 replacement with ``--to pep440``."""

    _install_git(monkeypatch, tags=["v1.2.3-beta.2"])
    result = runner.invoke(
        app,
        _command(tmp_path, "local", "--to", "pep440", "--yes"),
    )

    assert result.exit_code == 0
    assert "Destination format : pep440" in result.stdout
    assert "v1.2.3b2" in result.stdout


def test_existing_destination_stops_the_complete_plan(
    monkeypatch, tmp_path: Path
) -> None:
    """Never partially apply a plan containing an existing destination."""

    git = _install_git(
        monkeypatch,
        tags=["v1.2.3b1", "v1.2.3-beta.1"],
    )
    result = runner.invoke(app, _command(tmp_path, "local"))

    assert result.exit_code == 1
    assert "Planned            : 0" in result.stdout
    assert "destination tag already exists" in result.stdout
    assert "Resolve every collision" in result.stdout
    git.get_tag_snapshot.assert_not_called()
    git.replace_local_tags_atomically.assert_not_called()


def test_signed_tag_is_rejected_before_confirmation(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Never silently invalidate or strip an annotated-tag signature."""

    git = _install_git(monkeypatch, tags=["v1.2.3b1"], signed=True)
    result = runner.invoke(app, _command(tmp_path, "local", "--yes"))

    assert result.exit_code == 1
    assert "signed" in result.stdout
    assert "cannot rename" in result.stdout
    git.create_replacement_ref.assert_not_called()


def test_local_scope_rejects_repository_url(monkeypatch) -> None:
    """Reject a temporary URL checkout for a local-only replacement."""

    url = "https://github.com/example/project.git"
    result = runner.invoke(
        app,
        [
            "--no-banner",
            "--repository-url",
            url,
            "tags",
            "convert",
            "local",
        ],
    )

    assert result.exit_code != 0
    assert "requires a persistent local checkout" in result.stdout
    assert "Traceback" not in result.stdout


class _ConfigDouble:
    """Minimal CLI/config/default precedence double."""

    def __init__(self, values: dict[tuple[str, ...], object]) -> None:
        self.values = values

    def resolve(self, cli_value, config_keys, default=None):
        """Apply explicit CLI, configured value, then internal default."""

        if cli_value is not None:
            return cli_value
        return self.values.get(tuple(config_keys), default)


def _execution_args(tmp_path: Path) -> ReflowExecutionArgs:
    """Create shared execution arguments for resolver tests."""

    return ReflowExecutionArgs(
        dry_run=False,
        debug=False,
        log_level=LogLevelChoices.INFO,
        silent=False,
        repository=RepositoryTarget(path=tmp_path),
        progress_enabled=True,
    )


def test_resolver_defaults_to_semver_and_confirmation(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Keep SemVer as the default and preserve explicit local scope."""

    monkeypatch.setattr(
        "app.cli.commands.reflow.tags.convert.resolver.get_config",
        lambda: _ConfigDouble({}),
    )
    args = resolve_convert_tags_args(
        execution_args=_execution_args(tmp_path),
        scope=TagConversionScope.LOCAL,
    )

    assert args.scope is TagConversionScope.LOCAL
    assert args.target_format is TagFormat.SEMVER
    assert args.yes is False


def test_resolver_reads_shared_conversion_defaults_from_config(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Use one documented format/confirmation configuration for both scopes."""

    values = {
        ("cli", "tags", "convert", "target_format"): "pep-440",
        ("cli", "tags", "convert", "yes"): True,
    }
    monkeypatch.setattr(
        "app.cli.commands.reflow.tags.convert.resolver.get_config",
        lambda: _ConfigDouble(values),
    )
    args = resolve_convert_tags_args(
        execution_args=_execution_args(tmp_path),
        scope=TagConversionScope.REMOTE,
    )

    assert args.scope is TagConversionScope.REMOTE
    assert args.target_format is TagFormat.PEP440
    assert args.yes is True


def test_resolver_rejects_invalid_configured_format(
    monkeypatch,
    tmp_path: Path,
) -> None:
    """Report invalid configured formats as configuration errors."""

    monkeypatch.setattr(
        "app.cli.commands.reflow.tags.convert.resolver.get_config",
        lambda: _ConfigDouble({("cli", "tags", "convert", "target_format"): "calver"}),
    )

    with pytest.raises(ConfigurationError, match="Unsupported tag format"):
        resolve_convert_tags_args(
            execution_args=_execution_args(tmp_path),
            scope=TagConversionScope.LOCAL,
        )

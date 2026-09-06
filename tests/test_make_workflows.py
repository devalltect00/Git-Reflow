# tests/test_make_workflows.py

"""Structural regression tests for Reflow's modular Make workflows."""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = PROJECT_ROOT / "Makefile"
MAKE_CORE = PROJECT_ROOT / "make" / "core"

EXPECTED_COMMAND_MODULES = {
    "setup_install/command.mk",
    "local/command.mk",
    "testing/command.mk",
    "lint_format/command.mk",
    "qa/command.mk",
    "ci/command.mk",
    "documentation/command.mk",
    "build_publish/command.mk",
    "docker/command/common.mk",
    "docker/command/core.mk",
    "compose/command/common.mk",
    "compose/command/core.mk",
    "remote/command/registry.mk",
    "remote/command/runtime.mk",
    "git/command.mk",
    "cleanup/command.mk",
}


def _read(relative_path: str) -> str:
    """Read a Make module using a path relative to ``make/core``."""

    return (MAKE_CORE / relative_path).read_text(encoding="utf-8")


def _target_names(text: str) -> set[str]:
    """Return explicit Make target names from module text."""

    targets: set[str] = set()
    for line in text.splitlines():
        if line.startswith(("\t", "#", ".")) or ":" not in line:
            continue
        target_text = line.split(":", maxsplit=1)[0]
        if "$" in target_text or "=" in target_text:
            continue
        targets.update(target_text.split())
    return targets


def _make_list(text: str, variable: str) -> set[str]:
    """Return words assigned to a simple or continued Make variable list."""

    lines = text.splitlines()
    prefix = f"{variable} :="
    for index, line in enumerate(lines):
        if not line.startswith(prefix):
            continue

        parts = [line.split(":=", maxsplit=1)[1].strip()]
        while parts[-1].endswith("\\"):
            index += 1
            parts.append(lines[index].strip())
        return set(" ".join(parts).replace("\\", "").split())

    raise AssertionError(f"Make variable list not found: {variable}")


def test_root_makefile_is_a_thin_module_loader() -> None:
    """The root Makefile should load every command module without owning them."""

    root_text = MAKEFILE.read_text(encoding="utf-8")

    assert len(root_text.splitlines()) < 60
    assert "ROOT_DIR := $(CURDIR)" in root_text
    for module in EXPECTED_COMMAND_MODULES:
        assert f"include make/core/{module}" in root_text


def test_local_reflow_commands_enable_utf8_console_output() -> None:
    """Make-driven Rich output should use UTF-8 on Windows and Unix."""

    variables = _read("variables/variable.mk")

    assert "set PYTHONUTF8=1&&" in variables
    assert "PYTHON_UTF8_PREFIX := PYTHONUTF8=1" in variables
    assert "LOCAL_RUN ?= $(PYTHON_UTF8_PREFIX)" in variables


def test_every_expected_make_module_exists() -> None:
    """The modular command and help layout should remain complete."""

    missing = [
        module
        for module in EXPECTED_COMMAND_MODULES
        if not (MAKE_CORE / module).is_file()
    ]
    assert missing == []

    command_groups = {
        path.parent.relative_to(MAKE_CORE).as_posix()
        for path in MAKE_CORE.rglob("command.mk")
    }
    help_groups = {
        path.parent.relative_to(MAKE_CORE).as_posix()
        for path in MAKE_CORE.rglob("help.mk")
    }
    assert {
        "setup_install",
        "local",
        "testing",
        "lint_format",
        "qa",
        "ci",
        "documentation",
        "build_publish",
        "git",
        "cleanup",
    }.issubset(command_groups & help_groups)


def test_runtime_targets_use_current_reflow_cli_commands() -> None:
    """Runtime modules should map aliases to the canonical Reflow commands."""

    modules = [
        _read("local/command.mk"),
        _read("docker/command/core.mk"),
        _read("compose/command/core.mk"),
        _read("remote/command/runtime.mk"),
    ]

    for text in modules:
        assert "releases recover" in text
        assert "tags convert local" in text
        assert "tags convert remote" in text
        assert "\n\t\tdockerize" in text
        assert not re.search(r"\\\n\t\ttags replay(?:\s|\\)", text)
        assert "REFLOW_COMPOSEIZE_ARGS" not in text


def test_each_reflow_workflow_has_a_dry_run_target() -> None:
    """Every supported runtime workflow should expose a dry-run Make target."""

    prefixes_and_modules = {
        "l": _read("local/command.mk"),
        "d": _read("docker/command/core.mk"),
        "c": _read("compose/command/core.mk"),
        "r": _read("remote/command/runtime.mk"),
    }

    for prefix, text in prefixes_and_modules.items():
        targets = _target_names(text)
        assert (
            f"{prefix}-init-dryrun" in targets
            or f"{prefix}-reflow-init-dryrun" in targets
        )
        assert f"{prefix}-reflow-releases-recover-dryrun" in targets
        assert f"{prefix}-reflow-tags-convert-dryrun" in targets
        assert f"{prefix}-reflow-tags-convert-local-dryrun" in targets
        assert f"{prefix}-reflow-tags-convert-remote-dryrun" in targets
        assert f"{prefix}-reflow-dockerize-dryrun" in targets
        assert "override " in text


def test_deprecated_replay_targets_delegate_to_release_recovery() -> None:
    """Legacy replay Make targets should warn and delegate, never call replay."""

    for relative_path in (
        "local/command.mk",
        "docker/command/core.mk",
        "compose/command/core.mk",
        "remote/command/runtime.mk",
    ):
        text = _read(relative_path)
        assert "is deprecated - use" in text
        assert "reflow-releases-recover" in text


def test_remote_registry_covers_the_shared_utility_catalog() -> None:
    """Remote registry commands should cover every shared Devalltect image."""

    variables = _read("variables/variable.mk")
    registry = _read("remote/command/registry.mk")

    expected_projects = {
        "PHS": "r-phs-pull",
        "DOC_GEN": "r-doc-gen-pull",
        "CUSTY": "r-custy-pull",
        "REFLOW": "r-reflow-pull",
    }
    for project, pull_target in expected_projects.items():
        assert f"REMOTE_IMAGE_{project} ?=" in variables
        assert f"REMOTE_{project}_REGISTRY_COMMANDS_LIST" in registry
        assert pull_target in _target_names(registry)


def test_remote_runtime_covers_all_projects_without_stale_custy_arguments() -> None:
    """Shared remote runtimes should be registered with project-owned args."""

    runtime = _read("remote/command/runtime.mk")
    targets = _target_names(runtime)

    expected_targets = {
        "r-phs-scan-apply-all",
        "r-doc-generate-smart",
        "r-custy-run-release",
        "r-reflow-releases-recover-dryrun",
    }
    assert expected_targets.issubset(targets)

    for group in ("PHS", "DOC_GEN", "CUSTY", "REFLOW"):
        assert f"REMOTE_{group}_RUNTIME_COMMANDS_LIST" in runtime

    custy_section = runtime.split("# Custy.", maxsplit=1)[1].split(
        "# Reflow.", maxsplit=1
    )[0]
    assert "REMOTE_CUSTY_INIT_ARGS" in custy_section
    assert "REMOTE_REFLOW_INIT_ARGS" not in custy_section


def test_remote_custy_runtime_uses_current_custy_cli_commands() -> None:
    """The shared Custy image wrapper should follow Custy's active CLI tree."""

    runtime = _read("remote/command/runtime.mk")
    custy_section = runtime.split("# Custy.", maxsplit=1)[1].split(
        "# Reflow.", maxsplit=1
    )[0]

    expected_commands = {
        "validate",
        "version update",
        "changelog generate",
        "backup commit",
        "backup tag",
        "backup all",
        "cleanup backups",
        "cleanup branches",
        "cleanup all",
        "workflow branch",
    }
    for command in expected_commands:
        assert f"\n\t\t{command} " in custy_section

    assert "r-custy-init-all-no-examples" in custy_section
    assert "REMOTE_CUSTY_RUN_SUBCOMMAND := apply_version" not in custy_section
    assert "REMOTE_CUSTY_RUN_SUBCOMMAND := changelog" not in custy_section


def test_container_utilities_prepare_and_reuse_development_images() -> None:
    """Docker and Compose utilities should build their required app images."""

    variables = _read("variables/variable.mk")
    docker_core = _read("docker/command/core.mk")
    compose_common = _read("compose/command/common.mk")
    compose_core = _read("compose/command/core.mk")

    assert "d-test: d-build-dev" in docker_core
    assert "$(COMPOSE_DEV) build $(SERVICE_APP)" in compose_common
    assert "$(COMPOSE_PROD) build $(SERVICE_APP)" in compose_common

    compose_utilities = {
        "c-test": "COMPOSE_DEV_RUN_TEST",
        "c-lint": "COMPOSE_DEV_RUN_LINT",
        "c-lint-fix": "COMPOSE_DEV_RUN_LINT_FIX",
        "c-format": "COMPOSE_DEV_RUN_FORMAT",
        "c-format-check": "COMPOSE_DEV_RUN_FORMAT_CHECK",
        "c-shell": "COMPOSE_DEV_RUN_SHELL",
        "c-build-package": "COMPOSE_DEV_RUN_BUILD",
    }
    for target, command_variable in compose_utilities.items():
        assert f"{target}: c-build-dev" in compose_core
        assert f"$({command_variable})" in compose_core
        assert f"{command_variable} :=" in variables

    assert "COMPOSE_DEV_UP_DOCS :=" in variables
    assert "$(COMPOSE_DEV_UP_DOCS) -d" in compose_core


def test_help_uses_custy_style_and_lists_each_remote_project() -> None:
    """Help output should use grouped totals and aligned command columns."""

    help_command = _read("help/command.mk")
    help_helper = _read("help/helper.mk")
    help_variables = _read("help/variable.mk")
    remote_help = _read("remote/help.mk")

    assert "Available Commands" in help_helper
    assert "$(call HELP_TOTAL,HELP)" in help_helper
    assert "HELP_COLUMN_SEPARATOR" in help_variables

    expected_help_targets = {
        "help-remote-phs-registry",
        "help-remote-phs-runtime",
        "help-remote-docgen-registry",
        "help-remote-docgen-runtime",
        "help-remote-custy-registry",
        "help-remote-custy-runtime",
        "help-remote-reflow-registry",
        "help-remote-reflow-runtime",
    }
    for target in expected_help_targets:
        assert target in help_command
        assert target in _target_names(remote_help)

    assert {"help-remote-registry", "help-remote-runtime"}.issubset(
        _target_names(remote_help)
    )
    assert "$(HELP_COLUMN_SEPARATOR)" in remote_help


def test_every_registered_remote_command_is_implemented_and_documented() -> None:
    """Remote command registries, targets, and help should remain synchronized."""

    registry = _read("remote/command/registry.mk")
    runtime = _read("remote/command/runtime.mk")
    remote_help = _read("remote/help.mk")

    registered: set[str] = set()
    for group in ("PHS", "DOC_GEN", "CUSTY", "REFLOW"):
        registered.update(
            _make_list(registry, f"REMOTE_{group}_REGISTRY_COMMANDS_LIST")
        )
        registered.update(_make_list(runtime, f"REMOTE_{group}_RUNTIME_COMMANDS_LIST"))

    implemented = _target_names(registry) | _target_names(runtime)
    assert registered.issubset(implemented)
    for target in registered:
        assert f"make {target}" in remote_help

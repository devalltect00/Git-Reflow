# tests/test_container_workflows.py

"""Structural regression tests for Reflow's container configuration."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    """Read a project file as UTF-8 text."""

    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_development_helpers_reuse_the_app_image() -> None:
    """Only the development app service should own the image build definition."""

    compose = _read("docker-compose.dev.yml")

    assert "x-development-service: &development-service" in compose
    assert compose.count("build: *development-build") == 1
    assert compose.count("<<: *development-service") == 10
    assert "extends:\n      service: app" not in compose


def test_dockerfile_validates_runtime_and_accepts_an_explicit_version() -> None:
    """Container builds should validate imports and support SCM version injection."""

    dockerfile = _read("Dockerfile")

    assert "ARG REFLOW_BUILD_VERSION" in dockerfile
    assert dockerfile.count("SETUPTOOLS_SCM_PRETEND_VERSION") == 2
    assert 'RUN python -c "from app.cli.main import app"' in dockerfile
    lines = dockerfile.splitlines()
    continued_instructions = [
        index
        for index, line in enumerate(lines[:-1])
        if line.rstrip().endswith("\\") and not line.lstrip().startswith("#")
    ]
    assert all(lines[index + 1].strip() for index in continued_instructions)


def test_published_images_receive_the_scm_package_version() -> None:
    """Development and production publishing should pass the resolved SCM version."""

    development = _read(".github/workflows/docker-dev.yml")
    production = _read(".github/workflows/docker-prod.yml")

    assert "python -m app.core.build.version" in development
    assert (
        "REFLOW_BUILD_VERSION=${{ steps.package-version.outputs.value }}" in development
    )
    assert "python -m app.core.build.version" in production
    assert "REFLOW_BUILD_VERSION=${{ steps.version.outputs.version }}" in production


def test_release_images_follow_the_annotated_tag_contract() -> None:
    """Production and release workflows should enforce reviewed release tags."""

    production = _read(".github/workflows/docker-prod.yml")
    release = _read(".github/workflows/release.yml")
    gitlab_production = _read(".gitlab/docker-prod.yml")
    gitlab_release = _read(".gitlab/release.yml")

    for text in (production, release, gitlab_production, gitlab_release):
        assert "annotated Git tag" in text
        assert "rc|dev|post" in text

    assert "branches:" not in production
    assert "steps.vars.outputs.image_name" in production
    assert "publish_latest" in production
    assert "type=sha" not in production
    assert "docker/dev/Dockerfile" not in _read(".gitlab/docker-dev.yml")
    assert "docker/prod/Dockerfile" not in gitlab_production
    assert "--target development" in _read(".gitlab/docker-dev.yml")
    assert "--target production" in gitlab_production
    assert 'description: "./RELEASE_NOTES.md"' in gitlab_release


def test_ignore_files_cover_project_local_pytest_workspaces() -> None:
    """Generated Pytest workspaces should stay outside Git and image contexts."""

    for ignore_file in (".gitignore", ".dockerignore"):
        text = _read(ignore_file)
        assert ".pytest-tmp-*/" in text

    assert "\ntools\n" not in _read(".gitignore")
    assert "\ntools\n" not in _read(".dockerignore")
    assert "\n/build/\n" in _read(".gitignore")
    assert "\n/build/\n" in _read(".dockerignore")


def test_images_do_not_bake_developer_reflow_configuration() -> None:
    """Container images should not embed host-specific repository settings."""

    dockerignore = _read(".dockerignore")

    assert ".config/reflow/config.toml" in dockerignore

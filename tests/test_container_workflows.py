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
    gitlab_package = _read(".gitlab/python-package.yml")

    for text in (production, release):
        assert "annotated Git tag" in text
        assert "rc|dev|post" in text

    assert "annotated Git tag" in gitlab_package
    assert "package:build" in gitlab_package
    assert "package:publish" in gitlab_package
    assert "CI_COMMIT_REF_PROTECTED" in gitlab_package
    assert "CI_JOB_TOKEN" in gitlab_package
    assert "scripts/ci/package_version.py" in gitlab_package
    assert (
        "Unprotected tag detected; validating package artifacts only" in gitlab_package
    )
    assert "publication requires a protected release tag" not in gitlab_package

    assert "branches:" not in production
    assert "steps.vars.outputs.image_name" in production
    assert "publish_latest" in production
    assert "type=sha" not in production
    assert "docker/dev/Dockerfile" not in _read(".gitlab/docker-dev.yml")
    assert "docker/prod/Dockerfile" not in gitlab_production
    assert "--target development" in _read(".gitlab/docker-dev.yml")
    assert "--target production" in gitlab_production
    assert "job: package:build" in gitlab_production
    assert "job: package:publish" in gitlab_release
    assert "job: docker:prod" in gitlab_release
    for protected_workflow in (
        gitlab_package,
        gitlab_production,
        gitlab_release,
    ):
        assert 'CI_COMMIT_REF_PROTECTED == "true"' in protected_workflow
    assert 'description: "./RELEASE_NOTES.md"' in gitlab_release
    assert "\\`$PACKAGE_VERSION\\`" in gitlab_release
    assert "      ```bash" not in gitlab_release

    # Markdown backticks inside an unquoted heredoc are Bash command
    # substitutions. Release-note generation must keep Docker examples literal.
    assert "cat <<EOF >> RELEASE_NOTES.md" not in release
    assert "printf '```bash\\n'" in release
    assert "docker pull ghcr.io/%s:%s\\n" in release
    assert "docker run --rm ghcr.io/%s:%s --help\\n" in release
    assert '"$IMAGE_NAME" "$IMAGE_TAG"' in release
    assert "- Version: `%s`\\n" in release
    assert "- Release Type: `%s`\\n" in release
    assert '"$GITHUB_REPOSITORY"' in release
    assert '"$GITHUB_WORKFLOW"' in release


def test_production_images_publish_stable_version_aliases_only() -> None:
    """Stable releases should move aliases without promoting prereleases."""

    github = _read(".github/workflows/docker-prod.yml")
    gitlab = _read(".gitlab/docker-prod.yml")
    stable_regex = "STABLE_TAG_REGEX='^v[0-9]+\\.[0-9]+\\.[0-9]+$'"

    assert stable_regex in github
    assert stable_regex in gitlab
    assert 'echo "major=$MAJOR" >> "$GITHUB_OUTPUT"' in github
    assert 'echo "minor=$MINOR" >> "$GITHUB_OUTPUT"' in github
    assert 'echo "publish_aliases=$PUBLISH_ALIASES" >> "$GITHUB_OUTPUT"' in github
    assert (
        "type=raw,value=v${{ steps.version.outputs.major }}."
        "${{ steps.version.outputs.minor }},"
        "enable=${{ steps.version.outputs.publish_aliases }}"
    ) in github
    assert (
        "type=raw,value=v${{ steps.version.outputs.major }},"
        "enable=${{ steps.version.outputs.publish_aliases }}"
    ) in github

    stable_condition = 'if printf \'%s\' "$TAG" | grep -Eq "$STABLE_TAG_REGEX"; then'
    stable_block = gitlab[gitlab.index(stable_condition) :]
    for alias in (
        '"$CI_REGISTRY_IMAGE:v$MAJOR.$MINOR"',
        '"$CI_REGISTRY_IMAGE:v$MAJOR"',
        '"$CI_REGISTRY_IMAGE:latest"',
    ):
        assert f'docker tag "$CI_REGISTRY_IMAGE:$IMAGE_TAG" {alias}' in stable_block
        assert f"docker push {alias}" in stable_block
    assert "Prerelease tag detected; stable aliases will not be updated." in gitlab


def test_gitlab_pipeline_includes_private_python_package_stages() -> None:
    """The root pipeline should order validated package publication safely."""

    pipeline = _read(".gitlab-ci.yml")
    package = _read(".gitlab/python-package.yml")

    for stage in ("test", "package", "docker", "publish", "release"):
        assert f"  - {stage}" in pipeline
    assert 'local: ".gitlab/python-package.yml"' in pipeline
    assert "python -m twine check dist/*" in package
    assert "SETUPTOOLS_SCM_PRETEND_VERSION" in package
    assert "--repository-url" in package
    assert "--skip-existing" not in package


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

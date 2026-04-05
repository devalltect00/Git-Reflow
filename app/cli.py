import typer

from app.core.orchestrator import Orchestrator
from app.utils.git import GitHelper
from app.utils.logging import setup_logging

app = typer.Typer(help="Reflow - Release Flow Orchestrator")


@app.callback()
def main():
    setup_logging()


@app.command(name="replay-tags")
def run(
    dry_run: bool = False,
    delay: int = 2,
    only_stable: bool = False,
    limit: int = None,
):
    """
    Replay tags to trigger workflows.
    """
    orchestrator = Orchestrator(dry_run=dry_run, delay=delay)
    orchestrator.run(only_stable=only_stable, limit=limit)


@app.command()
def convert_tags(
    dry_run: bool = False,
):
    """
    Convert PEP440 tags → SemVer tags.
    """
    git = GitHelper(dry_run=dry_run)

    if not git.is_git_repo():
        typer.echo("❌ Not a git repository")
        raise typer.Exit()

    git.convert_all_tags()

@app.command(name="dockerize")
def dockerize(
    # image: str = typer.Option(..., help="ghcr.io/user/repo"),
    dry_run: bool = typer.Option(False, help="Preview commands only"),
):
    """
    Build & push Docker images for all tags (sequential).
    Build & push Docker images based on .reflow.toml config.
    - Build per tag
    - Tag latest for newest version
    - Push
    - Cleanup local images (keep only latest)

    Supports:
    - GitHub (ghcr.io)
    - GitLab (registry.gitlab.com)
    - Both
    """

    from app.utils.git import GitHelper
    from app.services.docker import DockerService
    from app.utils.config import ReflowConfig

    git = GitHelper()
    docker = DockerService(dry_run=dry_run)

    # -------------------------
    # LOAD CONFIG
    # -------------------------
    config = ReflowConfig()
    config.validate()

    provider = config.provider
    gh_image = config.github_image
    gl_image = config.gitlab_image

    # -------------------------
    # GET TAGS
    # -------------------------
    tags = git.get_all_tags()

    if not tags:
        typer.echo("❌ No tags found")
        raise typer.Exit()

    # if not docker.is_logged_in():
    #     typer.echo("⚠️ Not logged in to ghcr.io")
    #     typer.echo("👉 Run: docker login ghcr.io")
    #     raise typer.Exit()

    # Sort tags (important for latest detection)
    # tags = sorted(tags)

    latest_tag = tags[-1]
    latest_clean = latest_tag.lstrip("v")

    typer.echo(f"📌 Provider: {provider}")
    typer.echo(f"📌 Latest tag detected: {latest_tag}")

    # -------------------------
    # PROCESS TAGS (SEQUENTIAL)
    # -------------------------
    for tag in tags:
        clean_tag = tag.lstrip("v")

        typer.echo(f"\n🔁 Processing {tag}")

        # =====================
        # GITHUB
        # =====================
        if provider in ("github", "both"):
            # 1. BUILD
            docker.build_image(gh_image, clean_tag)

            # 2. TAG LATEST (only for newest)
            if tag == latest_tag:
                docker.tag_image(gh_image, clean_tag, "latest")

            # 3. PUSH
            docker.push_image(gh_image, clean_tag)

            if tag == latest_tag:
                docker.push_image(gh_image, "latest")

            # 4. CLEANUP (important 🚨)
            if tag != latest_tag:
                docker.remove_local_image(gh_image, clean_tag)

        # =====================
        # GITLAB
        # =====================
        if provider in ("gitlab", "both"):
            # 1. BUILD
            docker.build_image(gl_image, clean_tag)

            # 2. TAG LATEST (only for newest)
            if tag == latest_tag:
                docker.tag_image(gl_image, clean_tag, "latest")

            # 3. PUSH
            docker.push_image(gl_image, clean_tag)

            if tag == latest_tag:
                docker.push_image(gl_image, "latest")

            # 4. CLEANUP (important 🚨)
            if tag != latest_tag:
                docker.remove_local_image(gl_image, clean_tag)

    typer.echo("\n🎉 Dockerize completed (sequential + clean)")

@app.command(name="init")
def init():
    """
    Initialize reflow in current project.
    """

    import os
    from pathlib import Path

    config_path = Path(".reflow.toml")

    if config_path.exists():
        typer.echo("⚠️ .reflow.toml already exists")
        raise typer.Exit()

    config_content = """
[project]
name = "repo_name"

[docker]
provider = "github" # github | gitlab | both

[github]
image = "ghcr.io/username/repo_name"

[gitlab]
image = "registry.gitlab.com/username/repo_name"

# -----------------------------------------------------------------------------#
# source: https://github.com/devalltect00/git_reflow/pkgs/container/git_reflow #
# -----------------------------------------------------------------------------#
"""

    config_path.write_text(config_content.strip())

    typer.echo("✅ Created .reflow.toml")

    # Basic checks
    if not Path(".git").exists():
        typer.echo("⚠️ Not a git repository")

    if not Path("Dockerfile").exists():
        typer.echo("⚠️ No Dockerfile found")

    typer.echo("🎉 Reflow initialized!")
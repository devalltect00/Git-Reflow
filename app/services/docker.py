import subprocess
import logging
import json
from pathlib import Path
from app.utils.dry_run_support import DryRunSupport

logger = logging.getLogger(__name__)


class DockerService(DryRunSupport):
    def __init__(self, dry_run: bool = False):
        super().__init__(dry_run=dry_run)

    # def is_logged_in(self, registry: str = "ghcr.io") -> bool:
    #     docker_config = Path.home() / ".docker" / "config.json"

    #     if not docker_config.exists():
    #         return False

    #     try:
    #         data = json.loads(docker_config.read_text())
    #         auths = data.get("auths", {})
    #         return registry in auths
    #     except Exception:
    #         return False

    # =========================
    # BUILD LOCAL IMAGE
    # =========================
    def build_image(self, image: str, tag: str):
        full = f"{image}:{tag}"
        logger.info(f"🐳 Building {full}")

        self.runner.run(
            ["docker", "build", "-t", full, "."],
            check=True,
        )

    # =========================
    # TAG IMAGE
    # =========================
    def tag_image(self, image: str, source_tag: str, target_tag: str):
        src = f"{image}:{source_tag}"
        tgt = f"{image}:{target_tag}"

        logger.info(f"🏷 Tagging {src} → {tgt}")

        self.runner.run(
            ["docker", "tag", src, tgt],
            check=True,
        )

    # =========================
    # PUSH IMAGE
    # =========================
    def push_image(self, image: str, tag: str):
        full = f"{image}:{tag}"
        logger.info(f"🚀 Pushing {full}")

        self.runner.run(
            ["docker", "push", full],
            check=True,
        )

    # =========================
    # REMOVE LOCAL IMAGE
    # =========================
    def remove_local_image(self, image: str, tag: str):
        full = f"{image}:{tag}"
        logger.info(f"🧹 Removing local image {full}")

        self.runner.run(
            ["docker", "rmi", "-f", full],
            check=False,  # don't break flow
        )
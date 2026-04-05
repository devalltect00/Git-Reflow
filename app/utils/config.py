import tomllib
from pathlib import Path


class ReflowConfig:
    def __init__(self, path: str = ".reflow.toml"):
        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError(
                "❌ .reflow.toml not found. Run `reflow init` first."
            )

        self.data = tomllib.loads(self.path.read_text())

    # -------------------------
    # DOCKER
    # -------------------------
    @property
    def provider(self) -> str:
        return self.data.get("docker", {}).get("provider", "github")

    # -------------------------
    # GITHUB
    # -------------------------
    @property
    def github_image(self) -> str | None:
        return self.data.get("github", {}).get("image")

    # -------------------------
    # GITLAB
    # -------------------------
    @property
    def gitlab_image(self) -> str | None:
        return self.data.get("gitlab", {}).get("image")

    # -------------------------
    # VALIDATION
    # -------------------------
    def validate(self):
        provider = self.provider

        if provider not in ("github", "gitlab", "both"):
            raise ValueError("Invalid provider. Use github | gitlab | both")

        if provider in ("github", "both") and not self.github_image:
            raise ValueError("Missing [github].image in config")

        if provider in ("gitlab", "both") and not self.gitlab_image:
            raise ValueError("Missing [gitlab].image in config")
import logging
import subprocess
import re
from pathlib import Path

from app.utils.dry_run_support import DryRunSupport

logger = logging.getLogger(__name__)


class GitHelper(DryRunSupport):
    def is_git_repo(self) -> bool:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_all_tags(self) -> list[str]:
        result = subprocess.run(
            ["git", "tag", "--sort=creatordate"],
            capture_output=True,
            text=True,
        )
        return result.stdout.strip().splitlines() if result.stdout else []

    # =========================
    # NEW: DELETE REMOTE TAG
    # =========================
    def delete_remote_tag(self, tag: str):
        logger.info(f"🗑 Deleting remote tag: {tag}")
        self.runner.run(
            ["git", "push", "origin", f":refs/tags/{tag}"],
            check=True,
        )

    # =========================
    # PUSH
    # =========================
    def push_tag(self, tag: str):
        logger.info(f"⬆️ Pushing tag: {tag}")
        self.runner.run(
            ["git", "push", "origin", tag],
            check=True,
        )

    # =========================
    # VERSION CONVERSION
    # =========================
    def pep440_to_semver_tag(self, tag: str) -> str | None:
        original = tag

        # Already SemVer → skip
        if "-" in tag and tag.startswith("v"):
            return tag

        tag = tag.lstrip("v")

        if "+" in tag:
            tag, meta = tag.split("+", 1)
        else:
            meta = None

        match = re.match(r"(\d+\.\d+\.\d+)", tag)
        if not match:
            return None

        base = match.group(1)
        rest = tag[len(base):]

        result = f"v{base}"

        # pre-release
        pre = re.search(r"(a|b|rc)(\d+)", rest)
        if pre:
            typ, num = pre.groups()
            mapping = {"a": "alpha", "b": "beta", "rc": "rc"}
            result += f"-{mapping[typ]}.{num}"

        # dev
        dev = re.search(r"\.dev(\d+)", rest)
        if dev:
            result += f"-dev.{dev.group(1)}"

        # post
        post = re.search(r"\.post(\d+)", rest)
        if post:
            result += f"-post.{post.group(1)}"

        if meta:
            result += f"+{meta}"

        return result

    def convert_tag(self, old_tag: str):
        new_tag = self.pep440_to_semver_tag(old_tag)

        if not new_tag or new_tag == old_tag:
            logger.info(f"⏭️ Skip: {old_tag}")
            return

        logger.info(f"🔄 {old_tag} → {new_tag}")

        sha = subprocess.check_output(
            ["git", "rev-list", "-n", "1", old_tag],
            text=True,
        ).strip()

        message = subprocess.check_output(
            ["git", "tag", "-l", "--format=%(contents)", old_tag],
            text=True,
        )

        msg_file = Path(".tag_msg_tmp.txt")
        msg_file.write_text(message or "", encoding="utf-8")

        # create new tag
        self.runner.run(
            ["git", "tag", "-a", new_tag, sha, "-F", str(msg_file)],
            check=True,
        )

        # push new tag
        self.push_tag(new_tag)

        # delete old tag (local + remote)
        logger.info(f"🧹 Removing old tag: {old_tag}")
        self.runner.run(["git", "tag", "-d", old_tag], check=True)
        self.delete_remote_tag(old_tag)

        msg_file.unlink(missing_ok=True)

    def convert_all_tags(self):
        tags = self.get_all_tags()
        logger.info(f"📦 Found {len(tags)} tags")

        for tag in tags:
            self.convert_tag(tag)
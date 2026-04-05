import logging
import time

from app.core.tag_processor import TagProcessor
from app.utils.git import GitHelper
from app.services.github import GitHubService

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, dry_run: bool = False, delay: int = 2):
        self.git = GitHelper(dry_run=dry_run)
        self.processor = TagProcessor()
        self.github = GitHubService()
        self.delay = delay

    def run(self, only_stable: bool = False, limit: int | None = None) -> None:
        logger.info("🚀 Starting reflow process...")

        if not self.git.is_git_repo():
            logger.error("❌ Not a git repository.")
            return

        tags = self.git.get_all_tags()
        logger.info(f"🔍 Found {len(tags)} total tags")

        valid_tags = self.processor.filter_valid_tags(tags)

        if only_stable:
            valid_tags = [t for t in valid_tags if "-" not in t]

        if limit:
            valid_tags = valid_tags[:limit]

        logger.info(f"✅ {len(valid_tags)} valid tags to process")

        for tag in valid_tags:
            self._process_tag(tag)

        logger.info("🎉 Reflow completed successfully!")

    def _process_tag(self, tag: str) -> None:
        logger.info(f"🔁 Processing tag: {tag}")

        # ✅ skip if already released
        if self.github.release_exists(tag):
            return

        # 🔥 IMPORTANT: force CI trigger
        self.git.delete_remote_tag(tag)
        self.git.push_tag(tag)

        logger.info(f"⏳ Waiting {self.delay}s...")
        time.sleep(self.delay)
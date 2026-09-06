# app/cli/help/reflow/dockerize/help.py

"""
Help text for:

    reflow dockerize
"""

DOCKERIZE_HELP = """
🐳 Build and Publish Docker Images

Build Docker images from repository tags
and publish them to configured registries.

────────────────────────────────────────

🧩 What this command does

• Reads repository tags
• Builds Docker images
• Pushes images to registries
• Creates latest image automatically
• Optionally removes local images

────────────────────────────────────────

📋 Workflow

1. Load Git tags
2. Build Docker image
3. Push image
4. Create latest image
5. Cleanup local images

────────────────────────────────────────

⚙️ Requirements

• Git installed
• Docker installed
• Registry authentication configured

────────────────────────────────────────

🧪 Examples

reflow dockerize

reflow --repository ../testing_reflow --dry-run dockerize

reflow --repository-url https://gitlab.com/acme/project.git --dry-run dockerize

────────────────────────────────────────

💡 Tips

• Verify registry credentials first
• Use --dry-run when testing
• Keep local images during debugging

────────────────────────────────────────

📚 Related Commands

reflow releases recover
reflow tags convert local
"""

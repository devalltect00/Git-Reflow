# Dockerize Releases

## Overview

The `reflow dockerize` command builds and publishes Docker images from Git tags.

The command uses repository version tags as the source of truth for image versions and publishes versioned container images to a supported container registry.

---

# Why This Command Exists

Most release workflows eventually produce deployable artifacts.

For containerized applications, those artifacts are Docker images.

Instead of manually:

1. Checking out tags
2. Building images
3. Tagging images
4. Pushing images

Reflow automates the entire workflow.

---

# What This Command Does

The command:

1. Opens the selected local checkout or temporarily clones the selected URL.
2. Reads Git tags.
3. Selects tags to process.
4. Builds each tag from a detached worktree.
5. Applies image tags.
6. Pushes images to a container registry.
7. Optionally removes local images.

The repository target and registry image are independent. For example,
`--repository-url https://github.com/acme/source.git` selects the source code,
while `[tool.reflow.github].image = "ghcr.io/acme/image"` selects the publishing
destination.

---

# High-Level Workflow

```text id="8rwprn"
Git Tags
     │
     ▼
Select Tags
     │
     ▼
Build Image
     │
     ▼
Tag Image
     │
     ▼
Push Image
     │
     ▼
Cleanup
```

---

# Example

Repository tags:

```text id="db0nlt"
v1.0.0
v1.1.0
v2.0.0
```

Configured image:

```text id="xg71pd"
ghcr.io/acme/my-app
```

Produced images:

```text id="04y6bg"
ghcr.io/acme/my-app:v1.0.0
ghcr.io/acme/my-app:v1.1.0
ghcr.io/acme/my-app:v2.0.0
```

---

# What This Command Does NOT Do

The command does not:

- Create Git tags
- Convert Git tags
- Replay releases
- Publish GitHub releases
- Modify commit history

If you need tag conversion:

```bash id="eckf1f"
reflow tags convert local
```

If you need release recovery:

```bash id="bmv15z"
reflow releases recover
```

---

# Current Registry Support

Current configuration supports:

## GitHub Container Registry

Configuration:

```toml id="rhtd5m"
[tool.reflow.docker]

provider = "github"

[tool.reflow.github]

image = "ghcr.io/acme/my-app"
```

Result:

```text id="v2mz8e"
ghcr.io/acme/my-app:v1.0.0
```

---

## GitLab Container Registry

Configuration:

```toml id="9g0jz7"
[tool.reflow.docker]

provider = "gitlab"

[tool.reflow.gitlab]

image = "registry.gitlab.com/acme/my-app"
```

Result:

```text id="m1lz5g"
registry.gitlab.com/acme/my-app:v1.0.0
```

---

# Current Tag Selection Behavior

Current implementation:

```text id="plgqai"
Reads repository tags
       ↓
Selects tags
       ↓
Processes tags
```

The exact selection logic depends on command options and resolver configuration.

---

# Typical Use Cases

## Release Publishing

Repository tags:

```text id="6e0ymr"
v1.0.0
v1.1.0
v2.0.0
```

Build and publish images for release consumption.

---

## Container Registry Migration

Move images into:

```text id="0lkgc8"
GHCR
GitLab Registry
```

while preserving release versions.

---

## CI/CD Artifact Generation

Generate deployable images from repository releases.

---

## Historical Release Recovery

Build images for previously released versions.

Example:

```text id="m31iyl"
v1.0.0
v1.1.0
v2.0.0
```

even if those images were never published before.

---

# Inputs

The command uses:

```text id="2r0kw1"
✓ Git repository
✓ Git tags
✓ Docker daemon
✓ Registry configuration
✓ Container registry credentials
```

---

# Outputs

The command produces:

```text id="gvv4ib"
✓ Docker images
✓ Registry tags
✓ Published container images
```

Example:

```text id="k56xjp"
ghcr.io/acme/my-app:v1.0.0
```

The final summary reports published and failed image-tag counts. A completely
successful run exits with code `0`. If any build, tag, push, or cleanup
operation fails, Reflow lists the affected `image:tag`, prints a concise reason,
and exits with code `1`. Normal output does not include an implementation
traceback; use global `--debug` and the configured log file when technical
diagnostics are needed.

Docker publication is not atomic across multiple tags. A later failure does not
remove images that were published successfully earlier in the same run, so a
partial-failure summary can contain both published and failed entries.

---

# Optional Cleanup

Configuration:

```toml id="o86b3y"
[tool.reflow.docker]

keep_local_images = false
```

Behavior:

```text id="tqhhmu"
Build
Push
Remove Local Image
```

---

Configuration:

```toml id="7gm1kx"
[tool.reflow.docker]

keep_local_images = true
```

Behavior:

```text id="k1hhui"
Build
Push
Keep Local Image
```

---

# Recommended Workflow

For most projects:

```text id="n1l1fa"
Convert Tags
      ↓
Recover Releases
      ↓
Dockerize Images
```

Example:

```bash id="c8qj84"
reflow tags convert local
```

```bash id="3vjlwm"
reflow releases recover
```

```bash id="qntgpd"
reflow dockerize
```

---

# Supported Providers

Current support:

```text id="6s2ay0"
✓ GitHub Container Registry
✓ GitLab Container Registry
```

---

# Future Possibilities

Potential future support:

```text id="phkgvj"
Docker Hub
AWS ECR
Azure ACR
Google Artifact Registry
Harbor
Quay
```

---

# Related Commands

Convert tags:

```bash id="l38fzh"
reflow tags convert local
```

Replay releases:

```bash id="9lw0fr"
reflow releases recover
```

---

# Next Reading

Continue with:

- workflow.md
- requirements.md
- examples.md
- faq.md

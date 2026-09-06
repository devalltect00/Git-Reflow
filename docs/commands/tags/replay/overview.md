# Replay Existing Tags

!!! warning "Deprecated command name"
    `reflow tags replay` is retained as a compatibility alias. Use
    `reflow releases recover` for new workflows. The new name makes the
    operation's purpose—recovering missing releases—explicit. CLI help and
    command execution both display the deprecation.

## Overview

The `reflow tags replay` command delegates to `reflow releases recover`. It is
not a separate workflow.

This command is primarily used to recover, rebuild, or re-trigger release automation that depends on Git tag events.

Reflow does not create new versions during recovery. The selected tag names and
commits remain the same, but their remote references are deleted and pushed
again so downstream systems can process the new tag-push event.

---

## Why This Command Exists

Many release pipelines are triggered when a Git tag is pushed.

Examples include:

- GitHub Actions
- GitLab CI/CD
- Release automation workflows
- Container build pipelines
- Artifact publishing workflows

Sometimes these pipelines fail or become unavailable.

Common situations include:

- Repository migration
- CI/CD migration
- Failed release workflows
- Missing GitHub releases
- Accidental release deletion
- Infrastructure outages

In these situations, existing tags may already be present, but the release automation never completed successfully.

The replay command allows those tags to be processed again without creating new versions.

---

## What The Canonical Command Does

The delegated `reflow releases recover` workflow:

1. Reads existing version tags.
2. Checks which tags do not have corresponding GitHub releases.
3. Deletes and re-pushes those selected remote tags.
4. Retriggers tag-based CI/CD release automation.

It does not directly create a release through the GitHub website. It retriggers
the repository's existing release workflow.

---

## What This Command Does NOT Do

The command does not:

- Create new versions
- Rename tags
- Convert tag formats
- Build Docker images
- Publish Docker images
- Modify application code
- Create new commits

If you need to convert version formats, use:

```bash
reflow tags convert local
```

If you need to build Docker images, use:

```bash
reflow dockerize
```

---

## Typical Use Cases

### Re-trigger GitHub Actions

A workflow failed during release creation.

Replay the tags to trigger the workflow again.

### Recover Missing Releases

Tags exist, but releases were never published successfully.

Replay the tags to rebuild release metadata.

### Repository Migration

A repository has been moved to a new location.

Replay existing tags so the new release automation processes them.

### CI/CD Migration

After migrating pipelines, replay tags so artifacts can be rebuilt.

---

## Inputs

The command uses:

- Local Git repository
- Existing Git tags
- Remote repository configuration

---

## Outputs

Depending on configuration and release state, the command may:

- Re-push Git tags
- Re-trigger release automation
- Re-trigger CI/CD workflows
- Recreate missing release artifacts

---

## Supported Providers

Current implementation supports:

- Git repositories
- GitHub release workflows

Additional providers may be added in future releases.

---

## Related Commands

### Convert Tags

Convert PEP 440 tags to Semantic Versioning.

```bash
reflow tags convert local
```

### Dockerize

Build and publish Docker images from repository tags.

```bash
reflow dockerize
```

---

## Next Reading

For implementation details, see:

- `workflow.md`
- `requirements.md`
- `examples.md`
- `faq.md`

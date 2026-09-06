# Replay Existing Tags FAQ

!!! warning "Deprecated compatibility alias"
    `reflow tags replay` is deprecated. Use `reflow releases recover` in all
    new commands, scripts, and documentation. The alias currently delegates to
    the same implementation and remains only to avoid breaking older scripts.

## Overview

This document answers common questions about the replay command.

If you are new to Reflow, start with:

- overview.md
- workflow.md

before reading this FAQ.

---

# General Questions

## What does the alias actually do?

The alias prints a deprecation warning and calls `reflow releases recover`.

The canonical command reads version tags, finds tags without GitHub releases,
deletes and re-pushes those selected remote tags, and retriggers tag-based
release automation. It does not create a GitHub release directly.

Examples:

- GitHub Actions
- Release pipelines
- Artifact publishing workflows

Replay does not create new versions.

---

## Does replay create new tags?

No.

Replay uses existing tags.

Legacy example:

Before:

```text
v1.0.0
v1.1.0
```

After:

```text
v1.0.0
v1.1.0
```

No new versions are created.

---

## Does replay rename tags?

No.

Replay never changes tag names.

If you need version conversion, use:

```bash
reflow tags convert local
```

---

## Does replay build Docker images?

No.

Replay only processes tags.

To build Docker images, use:

```bash
reflow dockerize
```

---

# Tag Processing

## Does replay process all tags?

By default:

Yes.

Example:

```bash
reflow tags replay
```

Use this canonical command instead:

```bash
reflow releases recover
```

All repository version tags are considered before existing releases are
filtered out.

---

## Can replay process only stable releases?

Yes.

Use:

```bash
reflow releases recover --only-stable
```

Included:

```text
v1.0.0
v2.0.0
```

Excluded:

```text
v2.0.0rc1
v2.0.0-beta1
v2.0.0-alpha1
```

---

## Can replay process only a limited number of tags?

Yes.

Example:

```bash
reflow releases recover --limit 10
```

Only the first ten selected tags will be processed.

---

## Can replay process a single tag?

Not currently.

Current implementation operates on collections of tags.

Future versions may support:

```bash
reflow releases recover --tag v1.2.0
```

---

## Can replay process a range of tags?

Not currently.

Possible future feature:

```bash
reflow releases recover \
    --from v1.0.0 \
    --to v2.0.0
```

---

# Release Questions

## Why would I replay tags?

Common reasons include:

- Failed release workflows
- Missing GitHub releases
- Repository migration
- CI/CD migration
- Release recovery

---

## What happens if a release already exists?

The orchestration layer evaluates release state and performs the appropriate replay action.

Replay is designed to safely recover release automation.

---

## What happens if a release is missing?

Replay allows downstream release automation to recreate missing release artifacts.

---

# Safety

## Is release recovery safe?

Release recovery changes remote tag references. Treat a live run as a
remote-mutating operation.

Replay does not:

- Create new versions
- Modify source code
- Create commits

It preserves the selected tag names and commits, but deletes and re-pushes their
remote references. Preview the exact selection first.

---

## Should I use dry-run first?

Yes.

Recommended:

```bash
reflow --dry-run releases recover
```

before processing large repositories.

---

## Can release recovery disrupt repository automation?

Yes. Re-pushed tags can rerun CI/CD, artifact publication, notifications, or
other tag-triggered automation. Always review a dry run and verify the selected
repository before approving the live operation.

---

# Requirements

## Do I need Git?

Yes.

Verify:

```bash
git --version
```

---

## Do I need GitHub CLI?

Yes.

Verify:

```bash
gh --version
```

---

## Do I need authentication?

Yes.

Verify:

```bash
gh auth status
```

Expected:

```text
Logged in to github.com
```

---

# Troubleshooting

## No tags found

Problem:

```text
No tags found
```

Solution:

Verify:

```bash
git tag
```

---

## Not a Git repository

Problem:

```text
fatal: not a git repository
```

Solution:

Run replay inside a Git repository.

---

## GitHub authentication failed

Problem:

```text
Authentication required
```

Solution:

```bash
gh auth login
```

---

## Permission denied

Problem:

```text
Permission denied
```

Possible causes:

- Missing repository access
- Invalid SSH key
- Invalid access token

---

# Future Features

Potential future enhancements:

- Replay a single tag
- Replay tag ranges
- Replay tags by date
- Replay preview reports
- Replay provider selection
- Enhanced recovery workflows

---

# Related Commands

Convert version tags:

```bash
reflow tags convert local
```

Build Docker images:

```bash
reflow dockerize
```

---

# Additional Reading

- overview.md
- workflow.md
- requirements.md
- examples.md

# Replay Existing Tags Examples

!!! warning "Deprecated command name"
    These examples use the canonical `reflow releases recover` command.
    `reflow tags replay` remains only as a compatibility alias and should not
    be used in new scripts.

## Overview

This document contains practical examples of the replay command.

Examples range from simple usage to common production scenarios.

---

# Basic Replay

Replay all tags found in the repository.

Command:

```bash
reflow releases recover
```

Workflow:

1. Load all tags.
2. Check release state.
3. Replay tags when necessary.
4. Continue until complete.

Example output:

```text
Processing v1.0.0
Processing v1.1.0
Processing v2.0.0

Completed successfully.
```

---

# Replay Stable Releases Only

Replay only production releases.

Command:

```bash
reflow releases recover --only-stable
```

Included:

```text
v1.0.0
v2.0.0
v3.0.0
```

Skipped:

```text
v3.1.0rc1
v3.1.0-beta1
v3.1.0-alpha1
```

Recommended when:

- Production repositories
- Large tag histories
- Release recovery

---

# Replay Limited Tags

Replay only a specific number of tags.

Command:

```bash
reflow releases recover --limit 10
```

Example:

Repository contains:

```text
100 tags
```

Command processes:

```text
10 tags
```

Useful for:

- Testing
- Validation
- Gradual migration

---

# Replay Stable Tags With Limit

Combine multiple options.

Command:

```bash
reflow releases recover --only-stable --limit 5
```

Workflow:

1. Select stable tags.
2. Keep first five.
3. Replay selected tags.

Useful for:

- Production validation
- Incremental recovery

---

# Dry Run

Preview replay operations without making changes.

Command:

```bash
reflow --dry-run releases recover
```

Expected behavior:

```text
Would replay:
  v1.0.0
  v1.1.0
  v2.0.0
```

No tags are modified.

Recommended before large operations.

---

# Repository Migration

Scenario:

A repository was moved to a new GitHub organization.

Problem:

```text
Tags exist.
Releases missing.
```

Solution:

```bash
reflow releases recover
```

Result:

```text
Tags replayed.
Release automation triggered.
Releases recreated.
```

---

# GitHub Actions Recovery

Scenario:

GitHub Actions failed during release creation.

Existing state:

```text
Tag exists.
Release missing.
```

Solution:

```bash
reflow releases recover
```

Result:

```text
Workflow runs again.
Release recreated.
```

---

# CI/CD Migration

Scenario:

A new CI/CD pipeline was introduced.

Existing tags:

```text
v1.0.0
v1.1.0
v2.0.0
```

Need:

```text
Artifacts rebuilt.
```

Solution:

```bash
reflow releases recover
```

Result:

```text
Pipeline triggered for every tag.
Artifacts rebuilt.
```

---

# Recommended Workflow

For production repositories:

Step 1:

```bash
reflow --dry-run releases recover
```

Step 2:

```bash
reflow releases recover --only-stable
```

Step 3:

```bash
reflow releases recover
```

This minimizes risk while validating behavior.

---

# Common Mistakes

## Running Outside A Repository

Problem:

```text
Not a Git repository
```

Solution:

```bash
cd your-project
```

Then run replay.

---

## Missing GitHub Authentication

Problem:

```text
GitHub release checks fail.
```

Verify:

```bash
gh auth status
```

Login:

```bash
gh auth login
```

---

## Replaying Too Many Tags

Large repositories may contain hundreds of tags.

Instead of:

```bash
reflow releases recover
```

consider:

```bash
reflow releases recover --limit 10
```

for initial testing.

---

# Recommended Commands

Development:

```bash
reflow releases recover --limit 5
```

Production:

```bash
reflow releases recover --only-stable
```

Validation:

```bash
reflow --dry-run releases recover
```

Full Recovery:

```bash
reflow releases recover
```

---

# Next Reading

Continue with:

- faq.md
- workflow.md
- requirements.md

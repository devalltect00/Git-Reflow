# Reflow Questions and Answers

This section answers common user questions about which repository Reflow
operates on, whether changes stay local or reach GitHub/GitLab, and how remote
URLs and container registries fit together.

## Topics

- [Repository targeting](repository-targeting.md): local paths, GitHub/GitLab
  URLs, remote effects, dry-run behavior, and authentication.
- [Troubleshooting](troubleshooting.md): clone failures, configuration
  conflicts, missing tags, and registry publishing problems.

## Quick answer

Use an existing checkout when you want persistent local files:

```bash
reflow -C ../testing_reflow --dry-run tags convert local
```

Use a URL when the repository is not cloned locally:

```bash
reflow --repository-url https://github.com/acme/project.git --dry-run tags convert remote
```

Reflow temporarily clones URL targets. `tags convert local` changes only a
persistent checkout, while `tags convert remote` performs the guarded atomic
remote replacement. Release recovery deliberately changes remote tags during a
live run, and `dockerize` publishes to the configured container registry.

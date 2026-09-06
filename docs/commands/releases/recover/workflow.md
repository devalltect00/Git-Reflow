# Release Recovery Workflow

## Data Flow

```mermaid
flowchart TD
    Target[Resolve target repository] --> Tags[Read version tags]
    Tags --> Filter[Filter stable tags and apply limit]
    Filter --> Release{GitHub release exists?}
    Release -->|Yes| Skip[Skip tag]
    Release -->|No| Delete[Delete tag from configured remote]
    Delete --> Push[Push the existing local tag]
    Push --> CI[Tag-driven CI/CD recreates release]
```

Repository resolution follows one priority for every workflow:

1. Global `--repository`, `--repo`, `-C`, or `--repository-url` option.
2. `[tool.reflow.repository].path` or `[tool.reflow.repository].url` in Reflow
   configuration.
3. The invocation directory.

URL targets are temporarily cloned before Git and GitHub CLI commands run. The
Reflow source checkout is not implicitly used as the target.

## Compatibility Alias

`reflow tags replay` delegates to the same implementation and prints a
deprecation warning. Existing scripts continue to work, but new scripts and
documentation should use `reflow releases recover`. The deprecation is visible
both in CLI help and when the alias is executed.

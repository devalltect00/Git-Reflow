# Repository targeting questions and answers

## Does `repository.path` update only a local project?

It selects an existing checkout. Whether a command changes local or external
state depends on the command. Tag conversion makes this choice explicit:

```powershell
reflow -C ../testing_reflow tags convert local
reflow -C ../testing_reflow tags convert remote
```

The first command replaces local tag refs only. The second uses the checkout's
configured Git remote and replaces remote refs only.

## Can Reflow use a GitHub or GitLab URL directly?

Yes, for commands whose result can persist externally:

```powershell
reflow --repository-url https://github.com/acme/project.git --dry-run tags convert remote
reflow --repository-url https://gitlab.com/acme/project.git --dry-run dockerize
```

Reflow clones all branches and tags into a managed temporary workspace, runs
the workflow, and removes the checkout. It uses Git, not a provider API, for
repository operations.

## Do I need to clone first?

| Need | Recommended target |
| --- | --- |
| Replace local tags or inspect persistent results | Clone, then use `-C` |
| Initialize project files | Clone, then use `-C` |
| Replace remote tags without keeping a checkout | URL plus `tags convert remote` |
| Repeated work or existing CI checkout | Existing checkout |
| One-off external workflow | URL |

`tags convert local` rejects `--repository-url`; local changes in a temporary
clone would disappear. `reflow init` rejects URLs for the same reason.

## How do I configure the target?

Choose exactly one field:

```toml
[tool.reflow.repository]
path = "../testing_reflow"
```

or:

```toml
[tool.reflow.repository]
url = "https://github.com/acme/project.git"
```

Explicit `--repository`/`-C` or `--repository-url` options override
configuration. Never embed credentials in a URL; use normal Git credential
helpers or SSH authentication.

## Why do I get a `path` and `url` mutually exclusive error?

Both settings are active. Reflow cannot safely guess whether you intend to
modify a persistent checkout or materialize a temporary URL clone. Comment out
the unused form:

```toml
# Local target
path = "../testing_reflow"
# url = "https://github.com/acme/project.git"
```

or:

```toml
# Remote URL target
# path = "../testing_reflow"
url = "https://github.com/acme/project.git"
```

The CLI reports this as a normal configuration error with a solution and exit
code 2; it does not display an implementation traceback.

## Which commands support URL targets?

| Command | URL | Live external effect |
| --- | --- | --- |
| `reflow tags convert local` | No | None |
| `reflow tags convert remote` | Yes | Atomic remote tag replacement |
| `reflow releases recover` | Yes | Deletes and re-pushes selected remote tags |
| `reflow tags replay` | Yes, deprecated alias | Same as release recovery |
| `reflow dockerize` | Yes | Publishes configured container images |
| `reflow init` | No | Writes files in a persistent checkout |

## How do I replace GitHub or GitLab tag names?

Preview first:

```powershell
reflow --repository-url https://github.com/acme/project.git --dry-run tags convert remote
```

Then apply after reviewing the target and mapping:

```powershell
reflow --repository-url https://github.com/acme/project.git tags convert remote
```

Use `--yes` only for reviewed non-interactive automation. The remote must allow
tag creation/deletion and atomic pushes. The operation does not rename provider
Release objects.

## What does dry-run do with a URL?

It still creates and removes a temporary clone so Reflow can inspect real tags,
objects, and remote refs. It creates no tag object, changes no local or remote
ref, publishes no image, and does not ask for mutation confirmation.

## Is `repository.url` the same as `github.image`?

No:

```toml
[tool.reflow.repository]
url = "https://github.com/acme/source-project.git"

[tool.reflow.docker]
provider = "github"

[tool.reflow.github]
image = "ghcr.io/acme/published-image"
```

The repository URL selects Git source and remote state. Image settings select a
container destination and never retarget Git operations.

## What exactly does `reflow releases recover` do?

It reads version tags, finds tags without corresponding GitHub releases,
deletes and re-pushes selected remote tags, and retriggers tag-based CI/CD
release automation. It does not directly create a GitHub Release through the
website or provider API.

`reflow tags replay` remains only as a deprecated compatibility alias and
prints a warning. Use `reflow releases recover` in new work.

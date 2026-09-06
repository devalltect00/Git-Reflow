# Command Examples

This page collects common Reflow command examples. Start with `--dry-run` for
operations that can change tags, releases, or container registries.

Global options such as `--dry-run`, `--repository`, and `--repository-url` must
appear before the command name.

## Convert Tags in a Local Checkout

Preview the default PEP 440-to-SemVer replacement:

```powershell
reflow --dry-run -C D:/project/testing_lab/testing_reflow tags convert local
```

Apply after an interactive confirmation:

```powershell
reflow -C D:/project/testing_lab/testing_reflow tags convert local
```

Apply without prompting after the plan has already been reviewed:

```powershell
reflow -C D:/project/testing_lab/testing_reflow tags convert local --yes
```

Convert SemVer tag names to PEP 440 locally:

```powershell
reflow -C D:/project/testing_lab/testing_reflow tags convert local --to pep440 --yes
```

The `local` scope changes only tags in the selected checkout. It never pushes
or deletes tags on GitHub or GitLab and does not accept `--repository-url`.

## Convert Remote Tags from a Local Checkout

Preview changes to the checkout's configured Git remote:

```powershell
reflow --dry-run -C D:/project/testing_lab/testing_reflow tags convert remote
```

Apply the remote replacement without prompting:

```powershell
reflow -C D:/project/testing_lab/testing_reflow tags convert remote --yes
```

Convert remote SemVer tag names to PEP 440:

```powershell
reflow -C D:/project/testing_lab/testing_reflow tags convert remote --to pep440 --yes
```

The `remote` scope atomically creates the destination remote tags and deletes
their source remote tags. It leaves the checkout's local tag references
unchanged.

## Convert Remote Tags Using a Repository URL

Reflow can create a temporary clone, so a manually created checkout is not
required for remote conversion.

Preview a GitHub repository:

```powershell
reflow --repository-url https://github.com/devalltect00/testing_reflow.git --dry-run tags convert remote
```

Apply the default PEP 440-to-SemVer replacement:

```powershell
reflow --repository-url https://github.com/devalltect00/testing_reflow.git tags convert remote --yes
```

Apply SemVer-to-PEP-440 replacement:

```powershell
reflow --repository-url https://github.com/devalltect00/testing_reflow.git tags convert remote --to pep440 --yes
```

The remote must support atomic pushes, and the authenticated user must be
allowed to create and delete tags. Reflow does not rename GitHub or GitLab
Release objects associated with the old tag names.

## Use Configuration-Based Targeting

Configure a persistent local checkout:

```toml
[tool.reflow.repository]
path = "D:/project/testing_lab/testing_reflow"

[tool.reflow.cli.tags.convert]
target_format = "semver"
yes = false
```

Then run:

```powershell
reflow --dry-run tags convert local
reflow tags convert local --yes
```

Alternatively, configure a repository URL:

```toml
[tool.reflow.repository]
url = "https://github.com/devalltect00/testing_reflow.git"

[tool.reflow.cli.tags.convert]
target_format = "semver"
yes = false
```

Then run the remote scope:

```powershell
reflow --dry-run tags convert remote
reflow tags convert remote --yes
```

Configure either `path` or `url`, never both. The conversion configuration is
shared by both scopes, but the `local` or `remote` command must always be chosen
explicitly.

If both values are uncommented, Reflow exits with a configuration error and
shows corrected local and remote examples. Fix the configuration by commenting
out the target form you are not using:

```toml
# Local checkout
path = "D:/project/testing_lab/testing_reflow"
# url = "https://github.com/devalltect00/testing_reflow.git"
```

or:

```toml
# Remote URL
# path = "D:/project/testing_lab/testing_reflow"
url = "https://github.com/devalltect00/testing_reflow.git"
```

## Other Common Commands

Initialize configuration in a local project:

```powershell
reflow -C D:/project/testing_lab/testing_reflow init
```

Preview release recovery from a repository URL:

```powershell
reflow --repository-url https://github.com/devalltect00/testing_reflow.git --dry-run releases recover
```

Preview Docker image processing:

```powershell
reflow --repository-url https://github.com/devalltect00/testing_reflow.git --dry-run dockerize
```

`reflow tags replay` is a deprecated compatibility alias. Use
`reflow releases recover` in new commands and automation.

## Configure Progress Output

Progress is enabled by default for initialization, remote cloning, tag
conversion, release recovery, and Docker publishing. Keep it visible during
interactive use:

```toml
[tool.reflow.cli.progress]
enabled = true
```

Disable the animation for redirected output or CI logs:

```toml
[tool.reflow.cli.progress]
enabled = false
```

This setting changes only terminal presentation. For example, this remains a
non-mutating preview whether progress is enabled or disabled:

```powershell
reflow --repository-url https://github.com/devalltect00/testing_reflow.git --dry-run tags convert remote
```

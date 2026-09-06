# Tag conversion examples

## Local checkout

Preview the default PEP 440-to-SemVer replacement:

```powershell
reflow -C D:/project/testing_lab/testing_reflow --dry-run tags convert local
```

Apply after interactive confirmation:

```powershell
reflow -C D:/project/testing_lab/testing_reflow tags convert local
```

Apply non-interactively:

```powershell
reflow -C D:/project/testing_lab/testing_reflow tags convert local --yes
```

Convert SemVer names to PEP 440 locally:

```powershell
reflow -C D:/project/testing_lab/testing_reflow tags convert local --to pep440 --yes
```

These commands never push or delete a remote tag.

## Remote repository

Preview through a GitHub URL:

```powershell
reflow --repository-url https://github.com/acme/project.git --dry-run tags convert remote
```

Apply one guarded atomic remote replacement:

```powershell
reflow --repository-url https://github.com/acme/project.git tags convert remote --yes
```

Use the `origin` remote from an existing checkout:

```powershell
reflow -C D:/project/acme-project --dry-run tags convert remote
reflow -C D:/project/acme-project tags convert remote --to pep440 --yes
```

The remote command leaves the checkout's local tag refs unchanged. Fetch or
prune tags afterward if you want the checkout to mirror the new remote names.

## Configuration defaults

```toml
[tool.reflow.cli.tags.convert]
target_format = "semver"
yes = false
```

`target_format` and `yes` are shared by both scoped commands. Scope is always a
command name and cannot be hidden in configuration.

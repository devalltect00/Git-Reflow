# Repository targeting troubleshooting

## How can I tell whether a long-running command is still working?

Reflow displays a spinner while cloning or inspecting a target and a
determinate progress bar for tag conversion stages, release-recovery tags, and
Docker publishing. Dry-run shows the same activity because it still performs
read-only discovery and simulation.

If animated progress is unsuitable for CI logs or redirected output, disable
the presentation globally:

```toml
[tool.reflow.cli.progress]
enabled = false
```

This does not cancel work, enable mutations, or weaken dry-run safeguards.

## Reflow says `path` and `url` are mutually exclusive

Keep exactly one entry under `[tool.reflow.repository]` and pass only one CLI
target. Do not combine `-C`/`--repository` with `--repository-url`.

Local configuration:

```toml
path = "D:/project/testing_lab/testing_reflow"
# url = "https://github.com/acme/project.git"
```

Remote URL configuration:

```toml
# path = "D:/project/testing_lab/testing_reflow"
url = "https://github.com/acme/project.git"
```

Reflow exits with code 2 and prints a corrective solution without an internal
traceback.

Command help remains available while correcting the configuration, for
example `reflow tags --help` and `reflow releases recover --help`. Reflow only
validates the operational repository target when a command is executed.

## Reflow says the repository URL is unsupported

Use a normal HTTPS, SSH, SCP-style SSH, or Git URL without embedded
credentials, spaces, queries, or fragments. Verify it independently with
`git clone` and use a credential helper or SSH agent for private repositories.

## `tags convert` did not change GitHub or GitLab

The local scope deliberately never changes a remote. Preview and run the remote
scope instead:

```powershell
reflow --repository-url https://github.com/acme/project.git --dry-run tags convert remote
reflow --repository-url https://github.com/acme/project.git tags convert remote --yes
```

## Why did older Reflow versions leave both tag names?

The former additive command created a destination and optionally deleted or
pushed tags through flags. The scoped replacement commands no longer have
`--push` or `--delete-old`. A successful operation leaves only the destination
name in the selected scope:

```powershell
reflow -C D:/project/testing_lab/testing_reflow tags convert local
reflow -C D:/project/testing_lab/testing_reflow tags convert remote
```

Local and remote are intentionally independent. Running `local` does not alter
remote names, and running `remote` does not alter local names.

## The destination tag already exists

Reflow stops the complete plan before mutation. It will not overwrite or merge
the destination, delete the source, or apply only the non-colliding mappings.
Inspect both refs and resolve the ambiguity manually before retrying.

## The tag is signed

Renaming changes an annotated tag's signed payload. Reflow refuses to invalidate
or strip that signature. Create and sign the desired replacement manually
according to your release policy.

## The remote rejected an atomic push

`tags convert remote` requires atomic-push support and permission to create and
delete tags. Protected-tag rules, stale source refs, insufficient permissions,
or unsupported atomic pushes cause the complete operation to fail. Reflow does
not retry using partial remote updates.

## `tags convert` is waiting for input

Live conversion asks for confirmation after displaying the target and mapping.
Use `--yes`/`-y` only in reviewed automation. Global `--dry-run` never prompts:

```powershell
reflow -C D:/project/testing_lab/testing_reflow --dry-run tags convert local
```

## I need SemVer tags converted to PEP 440

Use the reverse destination explicitly on either scope:

```powershell
reflow --dry-run tags convert local --to pep440
reflow tags convert remote --to pep440 --yes
```

## Reflow appears to target its own source repository

Check the target panel, then pass an explicit target before the command:

```powershell
reflow -C D:/project/testing_lab/testing_reflow --dry-run tags convert local
reflow --repository-url https://github.com/acme/project.git --dry-run tags convert remote
```

Without CLI or configured targeting, Reflow uses the invocation directory.

## `reflow init` rejects my URL

Initialization output must persist, while URL checkouts are temporary. Clone
first and select the checkout with `-C`.

## Release recovery cannot read GitHub releases

Run `gh auth status`. The authenticated identity must be able to read the
selected repository and push its tags. GitLab release recovery is not currently
implemented.

## Docker images are pushed under the wrong name

Repository selection and image selection are independent. Check
`[tool.reflow.repository]`, `[tool.reflow.docker].provider`, and the selected
provider's `image` value. An image name never retargets Git commands.

## Dockerize reports failed image tags

Reflow reports each failed `image:tag` with a concise build, tag, push, or
cleanup reason and exits with code 1 if any publication fails. It does not show
a success panel for a total failure, and normal command output omits internal
tracebacks.

Verify that Docker is running, every selected tag contains a usable Dockerfile,
the build context is valid, and the selected registry credentials have push
permission. Use `reflow --dry-run dockerize` to validate discovery and the plan.
Use global `--debug` and the configured log file for technical diagnostics.

Publication across multiple tags is not atomic. Images completed before a
later failure remain published and are shown in the partial-success count.

## No tags are found

Confirm the target and use `git ls-remote --tags <url>` for a remote. Reflow
cannot convert, recover, or dockerize versions if the selected repository has
no suitable tags.

## How can I test safely?

Place global `--dry-run` before the scoped command. Discovery and temporary URL
cloning may run, but no tag object, local ref, remote ref, provider release, or
registry image is changed.

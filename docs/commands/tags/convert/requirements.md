# Tag conversion requirements

## Common

- Python 3.14 or newer
- Git available on `PATH`
- A valid Git repository containing supported version-shaped tags
- Read access to tag refs and tag objects

## Local scope

`reflow tags convert local` requires a persistent checkout selected by the
current directory or `--repository`/`--repo`/`-C`. A repository URL is rejected.
The process needs permission to create Git objects and update local tag refs.

## Remote scope

`reflow tags convert remote` accepts a checkout with a configured remote or a
supported `--repository-url`. It additionally requires:

- credentials that can create and delete remote tags;
- a remote that supports atomic pushes;
- unchanged source refs between preflight and push;
- no existing destination refs.

Protected-tag policies can reject a live operation. Reflow reports that failure
and does not retry with a non-atomic partial update.

## Safety preflight

Run the same scoped command with global `--dry-run` first. Dry-run performs
read-only discovery and validation and may materialize a temporary URL clone,
but it creates no tag objects, updates no local refs, and pushes no remote refs.

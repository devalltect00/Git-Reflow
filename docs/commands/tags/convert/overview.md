# Tag conversion

Reflow converts supported version-shaped tag names between PEP 440 and
Semantic Versioning. Conversion is a tag-name replacement: the destination
name is created and the source name is removed in one local transaction or one
remote atomic push.

Choose the persistence scope explicitly:

```text
reflow tags convert local
reflow tags convert remote
```

`local` changes only a persistent local checkout and never contacts a remote
for mutation. It accepts the current checkout or `--repository`/`-C`, and
rejects `--repository-url` because a temporary clone is not a persistent local
target.

`remote` changes the selected repository's Git remote. It accepts either a
local checkout with a configured remote or `--repository-url`, which Reflow
materializes in a temporary workspace. The remote must support atomic pushes.

## Formats

SemVer is the default destination:

```text
v1.2.3b1  -> v1.2.3-beta.1
v1.2.3rc2 -> v1.2.3-rc.2
```

Use `--to pep440` for the reverse direction:

```text
v1.2.3-beta.1 -> v1.2.3b1
v1.2.3-rc.2   -> v1.2.3rc2
```

Unsupported or lossy mappings are skipped and explained. If any destination
tag already exists, Reflow stops the entire plan before mutation.

## Metadata and safety

- Lightweight tags remain lightweight and reference the same Git object.
- Unsigned annotated tags preserve their target object, target type, tagger
  identity, tagger timestamp, timezone, message, and optional encoding header.
- The tag name is part of an annotated tag object, so its object ID necessarily
  changes when the name changes.
- Signed annotated tags are rejected because renaming changes the signed
  payload and would invalidate the signature.
- Git cannot rename a ref in place. Reflow implements equivalent replacement
  semantics atomically; it does not perform an additive create-only conversion.
- GitHub or GitLab Release objects that refer to old tag names are not renamed
  through provider APIs.

Live operations display the target, mappings, scope, and mechanism, then ask
for confirmation. `--yes`/`-y` bypasses the prompt. Global `--dry-run` performs
discovery and validation but creates no tag object and changes no local or
remote ref.

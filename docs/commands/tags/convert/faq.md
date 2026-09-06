# Tag conversion FAQ

## Does Reflow truly rename a Git tag?

Git has no primitive that renames a tag ref in place. Reflow provides the
equivalent result by atomically creating the destination ref and deleting the
source ref. A successful scoped operation therefore leaves one tag name, not
both names.

## Why does an annotated tag get a new object ID?

The tag name is stored inside an annotated tag object. Changing that header
creates a new object ID. Reflow preserves the target, tagger identity, original
tagger date and timezone, message, and supported headers.

## What happens to lightweight tags?

They remain lightweight and point to the same object ID.

## What happens to signed tags?

Reflow stops before mutation. Renaming changes the signed payload, so retaining
the old signature would be misleading and stripping it would lose metadata.
Create and sign the replacement manually if that is your intended policy.

## Why did Reflow stop when a destination exists?

Replacing or merging an existing destination is ambiguous. Reflow treats every
destination collision as a hard stop for the complete plan, so it cannot delete
a source tag or apply only part of the requested conversion.

## Which command changes GitHub or GitLab tags?

Use the remote scope:

```powershell
reflow --repository-url https://github.com/acme/project.git tags convert remote --yes
```

The repository URL selects the Git repository. GHCR or GitLab registry image
configuration selects container destinations and never selects Git tag scope.

## Does remote conversion rename a GitHub or GitLab Release object?

No. It changes Git tag refs only. Provider-hosted Release objects associated
with the old tag name must be handled separately.

## Do I need a clone?

For `local`, yes: use a persistent checkout. For `remote`, no: a supported URL
can be cloned into Reflow's temporary workspace. An existing checkout is still
useful when you want normal Git credential and remote configuration.

## What does dry-run guarantee?

It may read tags, metadata, and remote refs and may create a temporary checkout,
but it does not run `git mktag`, update local refs, or push remote refs. It also
does not ask for mutation confirmation.

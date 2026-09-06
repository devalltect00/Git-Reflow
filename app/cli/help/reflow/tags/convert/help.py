# app/cli/help/reflow/tags/convert/help.py

"""Help text for the scoped tag-conversion command group."""

CONVERT_HELP = """
Convert Version Tags Safely

Convert target-repository tags between PEP 440 and Semantic Versioning.
SemVer is the default destination.

What this command does:

* Requires an explicit `local` or `remote` subcommand.
* Displays source-to-destination mappings before mutation.
* Preserves unsigned annotated metadata and lightweight-tag type.
* Rejects signed tags and destination collisions before mutation.
* Requires confirmation for live changes unless --yes is supplied.
* Uses one local ref transaction or one guarded atomic remote push.

Examples:

  reflow -C ../testing_reflow --dry-run tags convert local
  reflow -C ../testing_reflow tags convert local --to pep440 --yes
  reflow --repository-url https://github.com/acme/project.git --dry-run tags convert remote
  reflow --repository-url git@github.com:acme/project.git tags convert remote --yes

Tips:

* `local` never changes a remote and rejects --repository-url.
* `remote` leaves local tag refs unchanged.
* Dry-run creates no tag object and changes no local or remote ref.
* Unsupported or lossy mappings are skipped instead of guessed.
"""

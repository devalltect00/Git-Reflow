# CI/CD and release contract

Reflow uses the same release boundary on GitHub and GitLab: ordinary branch
commits may validate code or publish development images, but production images
and provider releases are created only from reviewed annotated version tags.

## Trigger matrix

| Workflow | Trigger | Persistent external effect |
| --- | --- | --- |
| CI | `main`, `develop`, merge requests, and every pushed tag | None |
| Python package gate | Any tag | Validates the annotated tag, builds canonical PEP 440 artifacts, and smoke-tests the wheel without publishing |
| Development image | `develop` or `dev` | Publishes `dev` and commit-SHA image tags |
| Production image | Validated protected release tag | Publishes the exact version tag; stable releases also update matching minor, major, and `latest` aliases |
| Private Python package | Validated protected release tag | Publishes one immutable wheel and sdist to the project GitLab PyPI registry |
| Provider release | Validated protected release tag | Creates a GitHub or GitLab release with package artifacts |

Reflow CI uses Python 3.14, which is also the package compatibility floor and
the standard container runtime.

## Release-tag requirements

The package gate stops unless all of these validation checks pass:

1. The tag follows the supported release policy described below.
2. The tag exists in the checked-out repository.
3. The tag is annotated rather than lightweight.
4. The annotated tag message contains non-whitespace release notes.
5. Wheel and sdist filenames and embedded metadata agree with the normalized
   package version.

An unprotected tag that passes these checks completes as a validation-only
pipeline. Its package artifacts are retained for inspection, but GitLab skips
the production image, package-registry upload, and release jobs. Those external
publication jobs additionally require the GitLab tag to be protected.

Manual GitHub runs require the name of an existing annotated tag. They do not
create or repair tags.

## Git tag and Python package versions

Repository tags may use the supported SemVer spelling or an already canonical
PEP 440 spelling. GitLab receives only canonical PEP 440 package metadata:

| Release tag | Python package version |
| --- | --- |
| `v1.2.3` | `1.2.3` |
| `v1.2.3-alpha.1` | `1.2.3a1` |
| `v1.2.3-beta.1` | `1.2.3b1` |
| `v1.2.3-rc.1` | `1.2.3rc1` |
| `v1.2.3-dev.1` | `1.2.3.dev1` |
| `v1.2.3.post1` | `1.2.3.post1` |

The package gate fails closed for unknown labels, missing numeric identifiers,
build metadata, and ambiguous spellings. For example, `v1.2.3-post.1` is not
converted because SemVer orders it as a prerelease while PEP 440 `.post1` is a
post-release. Use `v1.2.3.post1` when a Python post-release is intended.

## Private GitLab PyPI registry

`.gitlab/python-package.yml` builds and validates the wheel and source
distribution before any production publication. After the production image
succeeds, `package:publish` uploads both artifacts with GitLab's short-lived
`CI_JOB_TOKEN`. No package token is stored in the repository.

Unprotected tags run the same package checks but stop at validation. This keeps
temporary and fork pipelines informative without granting them publication
authority.

GitLab package versions are immutable. Re-running an upload for the same
distribution and version fails; the pipeline never overwrites or silently
skips an existing version.

Maintainers must protect the release-tag patterns used by the project. External
users should receive a deploy token with `read_package_registry`, while jobs in
authorized GitLab projects should use `CI_JOB_TOKEN`.

## Container image naming

Hosted workflows derive the image repository from the current provider project:

```text
GitHub: ghcr.io/<owner>/<repository>:<tag>
GitLab: $CI_REGISTRY_IMAGE:<tag>
```

This lets forks and disposable test repositories publish only within their own
registry namespace. No workflow contains the production project owner as a
hardcoded destination.

Prereleases publish only their exact image tag. A tag such as
`v1.0.0-rc.1` never updates stable aliases. A stable `v1.0.0` publication
creates `v1.0.0`, `v1.0`, `v1`, and `latest`. Pin automation to the immutable
exact tag; the other three names intentionally move with later stable releases.

## Release notes and artifacts

The complete annotated tag message becomes the public release description.
GitHub and GitLab then append release metadata, the exact container pull
command, and package-artifact information. Wheel and source-distribution
artifacts are built from the tagged source and published to the private GitLab
PyPI registry. GitLab release notes link to both the registry and retained build
artifacts.

## Planned 1.0 message sequence

The prepared Custy templates intentionally separate internal history from the
public release boundary:

1. Commit the comprehensive redesign with
   `commit-message-v1.0.0-development-checkpoint.txt`; do not tag it.
2. Commit the CI/CD finalization with `commit-message-v1.0.0-rc.1.txt`.
3. Create the annotated RC.1 tag from `tag-message-v1.0.0-rc.1.txt` on that
   CI/CD-finalization commit.
4. After RC validation, commit the stable-image alias work with
   `commit-message-v1.0.0-stabilization-checkpoint.txt`; do not tag it.
5. After final cleanup, use `commit-message-v1.0.0.txt` for the stable
   promotion commit.
6. Create the annotated stable tag from `tag-message-v1.0.0.txt`.

Development and stabilization checkpoints have no tag-message templates
because they are intentionally not release boundaries.

## Local validation

These checks validate the repository without publishing anything:

```bash
make check-ci
docker compose -f docker-compose.yml -f docker-compose.dev.yml config
docker compose -f docker-compose.yml -f docker-compose.prod.yml config
```

Container builds resolve a package version before `.git` is excluded from the
Docker build context:

```bash
python -m app.core.build.version
```

Do not test tag-triggered workflows against a production repository or registry
unless that external mutation has been explicitly approved.

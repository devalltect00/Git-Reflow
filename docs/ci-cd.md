# CI/CD and release contract

Reflow uses the same release boundary on GitHub and GitLab: ordinary branch
commits may validate code or publish development images, but production images
and provider releases are created only from reviewed annotated version tags.

## Trigger matrix

| Workflow | Trigger | Persistent external effect |
| --- | --- | --- |
| CI | `main`, `develop`, merge requests, and supported version tags | None |
| Development image | `develop` or `dev` | Publishes `dev` and commit-SHA image tags |
| Production image | Existing annotated `v*` release tag | Publishes the exact version tag; stable releases also update `latest` |
| Provider release | Existing annotated `v*` release tag | Creates a GitHub or GitLab release with package artifacts |

Reflow CI uses Python 3.14, which is also the package compatibility floor and
the standard container runtime.

## Release-tag requirements

Production and release jobs stop before publication unless all of these checks
pass:

1. The tag follows the supported SemVer-oriented form, such as `v1.0.0` or
   `v1.0.0-rc.1`.
2. The tag exists in the checked-out repository.
3. The tag is annotated rather than lightweight.
4. The annotated tag message contains non-whitespace release notes.
5. The package version resolved from Git agrees with the selected tag.

Manual GitHub runs require the name of an existing annotated tag. They do not
create or repair tags.

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
`v1.0.0-rc.1` never updates `latest`; only a stable tag such as `v1.0.0` does.

## Release notes and artifacts

The complete annotated tag message becomes the public release description.
GitHub and GitLab then append release metadata, the exact container pull
command, and package-artifact information. Wheel and source-distribution
artifacts are built from the tagged source.

## Planned 1.0 message sequence

The prepared Custy templates intentionally separate internal history from the
public release boundary:

1. Commit the comprehensive redesign with
   `commit-message-v1.0.0-development-checkpoint.txt`; do not tag it.
2. Commit the CI/CD finalization with `commit-message-v1.0.0-rc.1.txt`.
3. Create the annotated RC.1 tag from `tag-message-v1.0.0-rc.1.txt` on that
   CI/CD-finalization commit.
4. After RC validation and cleanup, use `commit-message-v1.0.0.txt` for the
   stable promotion commit.
5. Create the annotated stable tag from `tag-message-v1.0.0.txt`.

The checkpoint has no tag-message template because it is intentionally not a
release boundary.

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

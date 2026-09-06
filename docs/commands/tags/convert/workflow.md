# Tag conversion workflow

```mermaid
flowchart TD
    A[Resolve local or remote scope] --> B[Materialize target checkout]
    B --> C[Read and parse version tags]
    C --> D[Build source-to-destination plan]
    D --> E{Destination collision?}
    E -- Yes --> X[Stop complete plan]
    E -- No --> F[Snapshot source refs and metadata]
    F --> G{Signed tag?}
    G -- Yes --> X
    G -- No --> H{Dry-run?}
    H -- Yes --> I[Report plan; no mutation]
    H -- No --> J[Confirm unless --yes]
    J --> K{Scope}
    K -- Local --> L[Create objects then atomic update-ref]
    K -- Remote --> M[Create objects then guarded atomic push]
    L --> N[Verify destination exists and source is absent]
    M --> N
```

Planning and metadata inspection are read-only. For annotated tags, destination
objects are created only after confirmation. Object creation does not change a
ref; the visible replacement occurs at the atomic local or remote boundary.

Local replacement uses Git's reference transaction protocol. Remote
replacement sends destination creations and source deletions in one
`git push --atomic` operation with expected source object IDs. If the remote
does not support atomic pushes or its state changed, the complete update is
rejected rather than falling back to partial changes.

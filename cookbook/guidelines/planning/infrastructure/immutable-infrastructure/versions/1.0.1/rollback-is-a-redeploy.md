
- Rollback **MUST** be performed by redeploying the previous known-good image version, not by undoing changes on a live host.
- Keep prior image versions retained and addressable (immutable tags or digests, e.g. `app@sha256:...`) so any past release can be restored deterministically.
- Avoid mutable tags like `latest` for what is actually deployed; pin to an immutable digest or version tag.


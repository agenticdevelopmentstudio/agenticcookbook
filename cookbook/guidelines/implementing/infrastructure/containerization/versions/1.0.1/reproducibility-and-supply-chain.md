
- **pin-by-digest**: Base images SHOULD be pinned by digest, not a floating tag — `FROM python:3.13-slim@sha256:<digest>`. A tag like `:latest` is mutable; a digest is immutable and reproducible. Refresh digests deliberately (e.g., via Dependabot/Renovate) to pick up security patches.
- **deterministic-deps**: Install from a locked manifest (`requirements.txt` with hashes, `package-lock.json`, `go.sum`, `Cargo.lock`) so builds are repeatable.
- **rebuild-fresh**: Periodic release builds SHOULD use `--pull` (and `--no-cache` when patching) so stale base layers and dependencies do not persist.


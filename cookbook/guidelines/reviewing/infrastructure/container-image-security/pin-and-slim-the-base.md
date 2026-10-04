
- Base images **MUST** be pinned by immutable digest (`FROM image@sha256:...`), not by a mutable tag like `latest`. Tags are reassignable; digests are not.
- Prefer a minimal or distroless base (e.g. `distroless`, `alpine`, `wolfi`, or `scratch`) to shrink the attack surface — fewer packages means fewer CVEs and a smaller blast radius.
- Use multi-stage builds so compilers, build tools, and dev dependencies stay out of the final image.
- Rebuild on a cadence so base-image security patches actually reach production; a digest pin freezes patches as well as drift.


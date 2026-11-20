
- Run generation as a checked-in, reproducible step (a package script or task), not a one-off manual command.
- A drift check **SHOULD** run in CI: regenerate, then fail if the working tree differs from committed outputs. This guarantees outputs always match the source.
- Keep the transform configuration in version control alongside the token source.
- Reach for a managed token pipeline or design-tool sync service only when a measured need justifies it (per YAGNI); a local build step covers most projects.


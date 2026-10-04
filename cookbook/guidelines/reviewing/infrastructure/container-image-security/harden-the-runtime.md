
- The runtime **MUST** run as a non-root user; set an explicit `USER` and avoid UID 0.
- Secrets **MUST NOT** be baked into any layer — not in `ENV`, build args, or copied files. Layers are world-readable to anyone who pulls the image; inject secrets at runtime instead. Scan layer history (e.g. with a secret scanner) to confirm.
- Set a read-only root filesystem and drop unneeded Linux capabilities where the workload allows.
- Do not embed long-lived registry or cloud credentials in the image; use workload identity or short-lived tokens.

> Privacy and data-handling expectations around image contents are engineering guidance, not legal advice; consult counsel for regulatory obligations.


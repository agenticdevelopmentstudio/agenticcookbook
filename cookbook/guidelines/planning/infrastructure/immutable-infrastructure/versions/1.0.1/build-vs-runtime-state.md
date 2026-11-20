
- Bake application code and dependencies **into** the image at build time.
- Inject environment-specific config at **deploy/runtime** via environment variables or a config service — do not bake secrets or per-environment values into the image.
- Persistent data (databases, user uploads) **MUST** live in external, durable stores or attached volumes — never on the instance's ephemeral disk, which is destroyed on replace.


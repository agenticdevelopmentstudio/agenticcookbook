
- Provide a `.env.example` (committed, no real values) listing every variable the app reads; keep the real `.env` git-ignored and out of images.
- Validate and coerce config once at boot into a typed config object; the rest of the code reads that object, not `process.env`/`os.environ` directly.
- Inject secrets at runtime from a managed secret store (cloud secret manager, orchestrator secret, or vault) rather than baking them into the artifact. Treat the choice of a heavyweight secrets platform as adopt-when-measured-need-justifies, not a default (YAGNI) — start with environment injection.


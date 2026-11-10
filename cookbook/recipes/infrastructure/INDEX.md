# Infrastructure Recipes

Compositions of infrastructure ingredients into cross-cutting features.

| File | Description |
|------|-------------|
| [directory-sync/](directory-sync/) | Lifecycle pattern for syncing an in-memory file tree with the filesystem via cache, full sync, watch, and surgical update |
| [package-document/](package-document/) | Pattern for macOS document-based apps using directory bundle packages with SQLite databases and auto-save |
| [ai-processing-node/](ai-processing-node/) | Pull-model AI job worker: poll-claim loop, lease heartbeat, handler dispatch, structured-output LLM results, at-least-once idempotency |

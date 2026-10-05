# Infrastructure Ingredients

Atomic infrastructure patterns for persistence, logging, settings, directory sync, package documents and AI job processing.

| File | Description |
|------|-------------|
| [categorize-and-tag-handler.md](categorize-and-tag-handler.md) | Job handler that categorizes and tags a title and body with schema-constrained LLM output, idempotent per job ID |
| [directory-tree-cache.md](directory-tree-cache.md) | On-disk JSON cache of a flattened file tree, loaded off the main thread for instant display and written atomically |
| [directory-tree-scanner.md](directory-tree-scanner.md) | Builds a file tree from the filesystem with parallel top-level scanning and reloads only the directories affected by a change |
| [directory-watch-coordinator.md](directory-watch-coordinator.md) | Orchestrator that owns one directory's sync lifecycle and publishes its tree and syncing state, plus the workspace manager that pools one coordinator per directory entry |
| [filesystem-watcher.md](filesystem-watcher.md) | FSEvents-based file-level change monitor with debounce and configurable path exclusions |
| [job-worker.md](job-worker.md) | Pull-model job worker loop that claims typed jobs from a backend, renews leases with heartbeats, dispatches to handlers, and reports results with at-least-once idempotency |
| [llm-backend.md](llm-backend.md) | Configuration-selected inference backend (OpenAI-compatible HTTP endpoint or CLI subprocess) that returns schema-constrained structured output to job handlers |
| [logging.md](logging.md) | Centralized logging infrastructure with per-category static logger instances sharing one subsystem |
| [package-document-storage.md](package-document-storage.md) | SQLite-in-a-package storage format with schema versioning, legacy JSON migration, atomic temp-database writes, and migration-safe Codable models |
| [package-document-type.md](package-document-type.md) | Registers a directory-bundle document type with a custom UTType and wires it into DocumentGroup scenes with auto-save and session restoration |
| [settings-keys.md](settings-keys.md) | Centralized settings key registry with dot-notation naming to prevent key duplication and scattered string literals |
| [sqlite-helpers.md](sqlite-helpers.md) | Small SQLite utility layer with parameterized exec, row queries, last-insert id, temp database URLs, and a dedicated error type |
| [window-frame-persistence.md](window-frame-persistence.md) | Invisible view modifier that persists window position and size between sessions via frame autosave |

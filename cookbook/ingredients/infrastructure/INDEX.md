# Infrastructure Ingredients

Atomic infrastructure patterns for persistence, logging, settings, directory sync, package documents and AI job processing.

| File | Description |
|------|-------------|
| [categorize-and-tag-handler/](categorize-and-tag-handler/) | Job handler that categorizes and tags a title and body with schema-constrained LLM output, idempotent per job ID |
| [directory-tree-cache/](directory-tree-cache/) | On-disk JSON cache of a flattened file tree, loaded off the main thread for instant display and written atomically |
| [directory-tree-scanner/](directory-tree-scanner/) | Builds a file tree from the filesystem with parallel top-level scanning and reloads only the directories affected by a change |
| [directory-watch-coordinator/](directory-watch-coordinator/) | Orchestrator that owns one directory's sync lifecycle and publishes its tree and syncing state, plus the workspace manager that pools one coordinator per directory entry |
| [filesystem-watcher/](filesystem-watcher/) | FSEvents-based file-level change monitor with debounce and configurable path exclusions |
| [job-worker/](job-worker/) | Pull-model job worker loop that claims typed jobs from a backend, renews leases with heartbeats, dispatches to handlers, and reports results with at-least-once idempotency |
| [llm-backend/](llm-backend/) | Configuration-selected inference backend (OpenAI-compatible HTTP endpoint or CLI subprocess) that returns schema-constrained structured output to job handlers |
| [logging/](logging/) | Centralized logging infrastructure with per-category static logger instances sharing one subsystem |
| [package-document-storage/](package-document-storage/) | SQLite-in-a-package storage format with schema versioning, legacy JSON migration, atomic temp-database writes, and migration-safe Codable models |
| [package-document-type/](package-document-type/) | Registers a directory-bundle document type with a custom UTType and wires it into DocumentGroup scenes with auto-save and session restoration |
| [settings-keys/](settings-keys/) | Centralized settings key registry with dot-notation naming to prevent key duplication and scattered string literals |
| [sqlite-helpers/](sqlite-helpers/) | Small SQLite utility layer with parameterized exec, row queries, last-insert id, temp database URLs, and a dedicated error type |
| [window-frame-persistence/](window-frame-persistence/) | Invisible view modifier that persists window position and size between sessions via frame autosave |

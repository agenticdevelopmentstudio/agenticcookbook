---
id: AD558F24-29FA-430F-9EBD-0EC42F1AA9D1
title: "Package Document Storage"
domain: agenticdevelopercookbook://ingredients/infrastructure/package-document-storage
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "SQLite-in-a-package storage format with schema versioning, legacy JSON migration, atomic temp-database writes, and migration-safe Codable models"
platforms:
  - ios
  - macos
  - swift
  - windows
tags:
  - infrastructure
  - package-document
  - sqlite
  - migration
depends-on:
  - agenticdevelopercookbook://ingredients/infrastructure/sqlite-helpers
related:
  - agenticdevelopercookbook://recipes/infrastructure/package-document
  - agenticdevelopercookbook://ingredients/infrastructure/package-document-type
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Package Document Storage

## Overview

Package document storage defines what is inside a document package and how it is read and written: one or more SQLite database files holding all persistent state, versioned by `PRAGMA user_version`, with a fallback that reads legacy JSON files and migrates them to SQLite on the next save. Writes are atomic by construction — all data goes into a temporary SQLite file, its bytes are wrapped in a `FileWrapper`, and the system replaces the package directory in one step. Use it for each document type (project, workspace) that follows the structural pattern with its own database filename and schema.

### Terminology

| Term | Definition |
|------|-----------|
| Schema version | An integer stored in SQLite's `PRAGMA user_version` that identifies the database schema revision |
| Format migration | The process of reading a legacy format (e.g., JSON) and converting it to the current SQLite-based format on first save |
| Atomic write | Writing all data to a temporary SQLite file, reading it back as bytes, and wrapping it in a `FileWrapper` so the system can perform an atomic directory replacement |
| Key-value settings | A table of string key-value pairs used to store typed settings (booleans as `"true"`/`"false"`, numbers as string representations) |

### Architecture

```
┌─────────────────────────────────────────────────┐
│  DocumentGroup(newDocument:)                     │
│  ┌─────────────────────────────────────────────┐ │
│  │  ReferenceFileDocument                      │ │
│  │  ┌───────────────────────┐                  │ │
│  │  │  @Published var model │──objectWillChange│ │
│  │  └───────────┬───────────┘    → auto-save   │ │
│  │              │                              │ │
│  │  ┌───────────▼───────────┐                  │ │
│  │  │  fileWrapper(...)     │                  │ │
│  │  │  ┌─────────────────┐  │                  │ │
│  │  │  │ Temp SQLite DB  │  │                  │ │
│  │  │  │ → Insert data   │  │                  │ │
│  │  │  │ → Read bytes    │  │                  │ │
│  │  │  │ → FileWrapper   │  │                  │ │
│  │  │  └─────────────────┘  │                  │ │
│  │  └───────────────────────┘                  │ │
│  └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘

Package on disk:
┌──────────────────────────┐
│  MyDocument.catnip-proj/ │  ← Finder shows as single file
│  ├── project.db          │  ← SQLite database
│  └── (legacy: data.json) │  ← Removed after migration
└──────────────────────────┘
```

## Behavioral Requirements

### SQLite database schema

- **journal-mode-off**: The SQLite database MUST use `PRAGMA journal_mode = OFF` since the database resides inside a package and is not a standalone file.
- **pragma-user-version**: The SQLite database MUST use `PRAGMA user_version = N` to track the schema version, where N is an integer incremented with each schema change.
- **metadata-table**: The database MUST contain a `metadata` table with columns for document name (`TEXT`), schema version (`INTEGER`), and created date (`TEXT` in ISO 8601 format).
- **settings-table**: The database MUST contain a `settings` table with columns `key` (`TEXT PRIMARY KEY`) and `value` (`TEXT`) for key-value pair storage.
- **boolean-string-storage**: Boolean settings MUST be stored as the string values `"true"` or `"false"`.
- **numeric-string-storage**: Numeric settings MUST be stored as their string representations (e.g., `"42"`, `"3.14"`).
- **domain-specific-tables**: Domain-specific data tables MUST be defined per document type (e.g., sessions table for projects, file references for workspaces).

### Read process

- **check-sqlite-first**: On read, the document MUST first check the package `FileWrapper` for the expected SQLite database file (e.g., `project.db`).
- **fallback-legacy-json**: If the SQLite database file is not found, the document MUST check for a legacy JSON file (e.g., `data.json`) for backward compatibility.
- **deserialize-legacy-json**: If a legacy JSON file is found, the document MUST deserialize it and populate the model from JSON data. The next save will write SQLite format.
- **empty-package-defaults**: If neither SQLite nor legacy JSON files are found in the package, the document MUST treat it as a new empty document with default values.
- **log-format-version**: On successful read, the document MUST log the format version (SQLite schema version or "legacy JSON") at `info` level.

### Write process

- **temp-sqlite-write**: On write, the document MUST create a temporary SQLite database file at a unique path (UUID-based filename in the temporary directory).
- **parameterized-queries**: The document MUST insert all model data into the temporary database using parameterized queries.
- **read-temp-bytes**: After writing all data, the document MUST read the temporary database file contents as raw bytes (`Data`).
- **wrap-database-filewrapper**: The document MUST wrap the database bytes in a `FileWrapper(regularFileWithContents:)` with the `preferredFilename` set to the database filename (e.g., `project.db`).
- **directory-filewrapper**: The document MUST return a `FileWrapper(directoryWithFileWrappers:)` containing the database file wrapper, forming the package directory.
- **cleanup-temp-database**: The temporary database file MUST be deleted after its bytes have been read (cleanup in a `defer` block or equivalent).

### Migration-safe Codable

- **migration-safe-codable**: Model types that are deserialized from legacy JSON MUST implement custom `init(from decoder: Decoder)` with per-field `try`/`catch`, falling back to default values for any field that fails to decode.
- **model-version-field**: Each model type MUST include a `version` field (integer or string) for schema identification in both JSON and SQLite representations.
- **backward-compatible-schema**: Adding new settings fields to the model MUST NOT break deserialization of documents created with older versions of the schema.

## Appearance

Not applicable — this ingredient defines a storage and persistence format, not a visual component.

## States

| State | Behavior |
|-------|----------|
| New document | Empty model with default values; first save creates the package directory with a fresh SQLite database |
| Existing SQLite document | Read from SQLite database in the package; schema version checked against current version |
| Legacy JSON document | JSON file detected in the package; model populated from JSON; next save migrates to SQLite format |
| Corrupt database | SQLite open or query fails; document reports an error to the user and does not load |
| Missing database file | Neither SQLite nor JSON found in the package directory; treated as new empty document |
| Schema version mismatch (older) | Database `user_version` is lower than current; migration logic upgrades the schema on next save |
| Schema version mismatch (newer) | Database `user_version` is higher than current app version; document reports a version error and refuses to load |
| Writing | Model serialized to a temporary SQLite database, wrapped in a FileWrapper, and written to the package |

## Accessibility

Not applicable — this ingredient defines a storage format with no direct user interface. Error dialogs raised by the document inherit platform-standard accessibility from SwiftUI alert presentations.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pd-store-001 | journal-mode-off | Open the SQLite database inside a saved package | `PRAGMA journal_mode` returns `off` |
| pd-store-002 | pragma-user-version, metadata-table | Open the SQLite database and query `PRAGMA user_version` and `SELECT * FROM metadata` | `user_version` matches expected schema version; metadata row contains name, version, created_date |
| pd-store-003 | settings-table, boolean-string-storage, numeric-string-storage | Insert boolean setting `autoSave = true` and numeric setting `fontSize = 14` | Settings table contains `("autoSave", "true")` and `("fontSize", "14")` |
| pd-store-004 | check-sqlite-first | Open a package containing `project.db` | Document reads from SQLite successfully |
| pd-store-005 | fallback-legacy-json, deserialize-legacy-json | Open a package containing `data.json` but no `project.db` | Document reads from JSON; model is populated correctly |
| pd-store-006 | deserialize-legacy-json | Open a legacy JSON package, modify model, trigger save | Saved package contains `project.db` (SQLite); legacy JSON format replaced |
| pd-store-007 | empty-package-defaults | Open an empty package directory (no `project.db`, no `data.json`) | Document initializes with default values |
| pd-store-008 | log-format-version | Open a SQLite document with schema version 3 | Log entry: `info` level, includes "schema version 3" |
| pd-store-009 | temp-sqlite-write, parameterized-queries, read-temp-bytes | Trigger a save on a document with model data | Temporary SQLite file is created, data is inserted with parameterized queries, bytes are read |
| pd-store-010 | wrap-database-filewrapper, directory-filewrapper | Inspect the FileWrapper returned from `fileWrapper(...)` | Directory FileWrapper with one child whose `preferredFilename` is `project.db` |
| pd-store-011 | cleanup-temp-database | Trigger a save and inspect the temporary directory afterward | No leftover temporary `.db` files remain |
| pd-store-012 | migration-safe-codable, backward-compatible-schema | Deserialize a legacy JSON document that is missing a field added in a newer schema version | Missing field falls back to its default value; no crash or error |
| pd-store-013 | migration-safe-codable, backward-compatible-schema | Deserialize a legacy JSON document that contains an unknown extra field | Extra field is ignored; known fields are populated correctly |
| pd-store-014 | model-version-field | Inspect the model after reading from either JSON or SQLite | Model's `version` field is populated and matches the source's schema version |
| pd-store-015 | domain-specific-tables | Save a project document with sessions | The database contains the project's domain-specific table alongside `metadata` and `settings` |

## Edge Cases

- **Corrupt SQLite database**: If `sqlite3_open` succeeds but queries fail (e.g., malformed schema, incomplete write), the document MUST surface a user-facing error describing the corruption and MUST NOT overwrite the corrupt file. The user should be offered the option to create a new document or attempt manual recovery.
- **Missing files in package**: If the package directory exists but contains neither the expected SQLite database nor a legacy JSON file, the document treats this as a new empty document (empty-package-defaults). If the package directory itself is missing or inaccessible, the system reports a file-not-found error.
- **Format migration (JSON to SQLite)**: When a legacy JSON document is opened, the model is populated from JSON. On the next save, the write process creates a SQLite database. The legacy JSON file is not explicitly deleted from the package — the new `FileWrapper(directoryWithFileWrappers:)` simply omits it, and the atomic directory replacement removes it.
- **Disk full during write**: If the temporary SQLite file cannot be fully written due to insufficient disk space, the `exec()` call will fail. The document MUST catch this error and surface it to the user. The existing on-disk package MUST NOT be modified or corrupted.
- **Very large documents**: For documents with tens of thousands of rows, the write process creates the entire database in a temporary file. If memory pressure is a concern, the implementation SHOULD write incrementally and monitor for memory warnings on iOS.
- **Schema downgrade attempt**: If a document's `user_version` is higher than the app's current schema version, the document MUST refuse to load and present an error indicating that a newer version of the app is required (see States table).
- **Temporary file cleanup failure**: If the temporary database file cannot be deleted after reading its bytes, the operation SHOULD still succeed (the data was already captured). The leftover temp file will be cleaned up by the OS eventually.
- **Empty settings table**: If the settings table exists but contains no rows, all settings MUST fall back to their coded default values. This is not an error condition.
- **Date parsing failures**: If a date string in the metadata table does not conform to ISO 8601, the `invalidDate` error MUST be thrown and surfaced, rather than silently using a fallback date.
- **Multiple database files in package**: If future versions add additional database files to the package (e.g., `cache.db`), the read/write process MUST handle the presence of unknown files gracefully — they are preserved in the directory FileWrapper during write.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `databaseFileName` | string | (required, per document type) | Name of the SQLite file inside the package (e.g., `project.db`) |
| `legacyJSONFileName` | string | (none) | Name of the legacy JSON file read as a fallback (e.g., `data.json`) |
| `currentSchemaVersion` | integer | (required) | Highest `PRAGMA user_version` this app version supports |

## Logging

Subsystem: `{{bundle_id}}` | Category: `PackageDocument`

| Event | Level | Message |
|-------|-------|---------|
| Document opened (SQLite) | info | `PackageDocument: opened "{{filename}}" (SQLite schema version {{version}})` |
| Document opened (legacy JSON) | info | `PackageDocument: opened "{{filename}}" (legacy JSON format)` |
| Document opened (empty package) | info | `PackageDocument: opened "{{filename}}" (empty package, defaults applied)` |
| Write started | debug | `PackageDocument: write started for "{{filename}}"` |
| Temp database created | debug | `PackageDocument: temp database created at "{{tempPath}}"` |
| Data inserted | debug | `PackageDocument: inserted {{rowCount}} rows into {{tableName}}` |
| Temp database bytes read | debug | `PackageDocument: read {{byteCount}} bytes from temp database` |
| Temp database cleaned up | debug | `PackageDocument: temp database deleted at "{{tempPath}}"` |
| Write completed | debug | `PackageDocument: write completed for "{{filename}}"` |
| Legacy migration triggered | info | `PackageDocument: migrating "{{filename}}" from legacy JSON to SQLite` |
| Schema migration triggered | info | `PackageDocument: migrating "{{filename}}" from schema version {{oldVersion}} to {{newVersion}}` |
| Corrupt database detected | error | `PackageDocument: corrupt database in "{{filename}}": {{error}}` |
| Schema version too new | error | `PackageDocument: "{{filename}}" has schema version {{version}}, app supports up to {{maxVersion}}` |
| Disk full during write | error | `PackageDocument: write failed for "{{filename}}": disk full or I/O error: {{error}}` |
| Temp file cleanup failed | warning | `PackageDocument: failed to delete temp database at "{{tempPath}}": {{error}}` |
| Date parsing failed | error | `PackageDocument: invalid date string "{{dateString}}" in metadata table` |

## Platform Notes

- **macOS (SwiftUI)**: Use `FileWrapper(directoryWithFileWrappers:)` for the package and `FileWrapper(regularFileWithContents:)` for each file inside it. For atomic writes, the temporary database lives in the temporary directory and its bytes are handed to the `FileWrapper`; the system performs the atomic replacement.
- **macOS (AppKit)**: Override `read(from:ofType:)` and `fileWrapper(ofType:)` on `NSDocument` with the same SQLite read/write logic.
- **iOS / visionOS**: The same SQLite read/write logic applies. No platform-specific changes to the storage layer.
- **Windows**: The pattern is an ordinary directory containing a SQLite file; the same schema, versioning, and temp-file-then-replace write apply, using the platform's atomic rename.
- **Compose / React/Web**: Not applicable — the package and `FileWrapper` model are Apple-specific.

## Design Decisions

**Decision**: Write to a temporary SQLite file, read it back as bytes, and hand the bytes to a `FileWrapper`.
**Rationale**: SQLite wants a file path, while `ReferenceFileDocument` wants a `FileWrapper`. Going through a temporary file lets SQLite do what it does best while the document system performs the atomic directory replacement, so an interrupted write never corrupts the existing package.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [data-integrity](agenticdevelopercookbook://compliance/reliability#data-integrity) | partial | Reliability |
| [state-recovery](agenticdevelopercookbook://compliance/reliability#state-recovery) | partial | Reliability |
| [secure-data-storage](agenticdevelopercookbook://compliance/privacy-and-data#secure-data-storage) | partial | Privacy |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Package Document recipe |

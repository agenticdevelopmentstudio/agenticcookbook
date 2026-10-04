---
id: b2ba3ab9-743f-4c86-a75f-cc2e93fd3b07
title: "Package Document"
domain: agenticdevelopercookbook://recipes/infrastructure/package-document
type: recipe
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-03-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pattern for macOS document-based apps using directory bundle packages with SQLite databases and auto-save"
platforms:
  - ios
  - macos
  - swift
  - windows
tags:
  - infrastructure
  - package-document
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# Package Document

## Overview

A pattern for macOS document-based apps that use directory bundle packages (rendered as single files in Finder) containing SQLite databases. The document is a folder with a custom UTType conforming to `com.apple.package`, registered with a file extension (e.g., `.catnip-proj`, `.catnip-workspace`). Inside the package, one or more SQLite database files store all persistent state. The pattern supports schema versioning via `PRAGMA user_version`, format migration from legacy JSON files to SQLite, atomic writes through temporary database creation and `FileWrapper` packaging, and auto-save via SwiftUI's `ReferenceFileDocument` protocol. Each document type (project, workspace) follows the same structural pattern with its own UTType, file extension, database filename, and schema.

## Terminology

| Term | Definition |
|------|-----------|
| Package document | A directory bundle that macOS presents as a single file in Finder, identified by a custom UTType conforming to `com.apple.package` |
| UTType | A Uniform Type Identifier declared in Info.plist that maps a file extension to a content type and conformance hierarchy |
| ReferenceFileDocument | A SwiftUI protocol for reference-type documents that triggers auto-save when the document's `objectWillChange` publisher fires |
| FileWrapper | An Apple framework class representing a file, directory, or symbolic link in memory; used to read from and write to package directories |
| Schema version | An integer stored in SQLite's `PRAGMA user_version` that identifies the database schema revision |
| Format migration | The process of reading a legacy format (e.g., JSON) and converting it to the current SQLite-based format on first save |
| Atomic write | Writing all data to a temporary SQLite file, reading it back as bytes, and wrapping it in a FileWrapper so the system can perform an atomic directory replacement |
| Key-value settings | A table of string key-value pairs used to store typed settings (booleans as `"true"`/`"false"`, numbers as string representations) |
| Document scene | A SwiftUI `DocumentGroup` scene that manages the open/save/close lifecycle for a document type |

## Architecture

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

## UTType Registration

### Info.plist exported type declaration

Each document type requires an exported UTType entry in Info.plist:

```
UTExportedTypeDeclarations:
  - UTTypeIdentifier: com.example.catnip-project
    UTTypeDescription: Catnip Project
    UTTypeConformsTo: [com.apple.package]
    UTTypeTagSpecification:
      public.filename-extension: [catnip-proj]
```

### Swift UTType extension

```swift
extension UTType {
    static let catnipProject = UTType(exportedAs: "com.example.catnip-project")
    static let catnipWorkspace = UTType(exportedAs: "com.example.catnip-workspace")
}
```

## Behavioral Requirements

### UTType registration

- **package-uttype-declaration**: Each document type MUST declare a custom UTType conforming to `com.apple.package` in the app's Info.plist as an exported type.
- **unique-file-extension**: Each UTType MUST specify a unique file extension in `UTTypeTagSpecification` under `public.filename-extension`.
- **swift-uttype-property**: The UTType MUST be declared as a Swift `UTType` static property via `UTType(exportedAs:)` for use in document and file panel APIs.

### Document protocol conformance

- **reference-file-document**: Each document class MUST conform to `ReferenceFileDocument` (SwiftUI) and declare its `readableContentTypes` and `writableContentTypes` as the corresponding custom UTType.
- **published-model-property**: The document MUST expose a `@Published var model` property whose changes trigger `objectWillChange`, enabling SwiftUI auto-save.
- **filewrapper-read-write**: The document MUST implement `init(configuration:)` to read from a `FileWrapper` and `fileWrapper(snapshot:configuration:)` to write to a `FileWrapper`.

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

### SQLite helper utilities

- **temp-database-url-helper**: The codebase MUST provide a `tempDatabaseURL()` helper that returns a URL in the temporary directory with a UUID-based filename and `.db` extension.
- **exec-with-bindings**: The codebase MUST provide an `exec()` function that executes a SQL statement with parameterized bindings (supporting at minimum `.text(String)`, `.int(Int)`, and `.null` binding types).
- **query-functions**: The codebase MUST provide `queryRow()` and `queryAll()` functions for reading single and multiple rows from the database.
- **last-insert-row-id**: The codebase MUST provide a `lastInsertRowID()` function to retrieve the row ID of the last inserted row.
- **sqlite-error-type**: SQLite errors MUST be represented as a dedicated error type with cases for: `cannotOpen`, `execFailed`, `missingData`, and `invalidDate`.

### Document scenes

- **document-group-scene**: The app MUST declare a `DocumentGroup(newDocument:)` scene for each document type, associating it with the correct `ReferenceFileDocument` subclass.
- **non-document-window-group**: Non-document windows (e.g., settings, welcome screen) MUST use `WindowGroup` scenes, not `DocumentGroup`.
- **custom-menu-save-panel**: Custom menu commands for creating new documents MUST use `NSSavePanel` to select the save location and then programmatically create the document.

### Lifecycle

- **autosave-via-published**: Auto-save MUST be triggered automatically by the `@Published` model property's `objectWillChange` publisher. No manual save action is required from the user.
- **save-open-urls-on-quit**: On application quit, the document system MUST save the URLs of all currently open documents for session restoration.
- **restore-urls-on-launch**: On application launch, the document system MUST attempt to reopen previously saved document URLs, logging any that fail to open.

## Appearance

Not applicable — this recipe defines a storage and persistence pattern, not a visual component.

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
| Auto-save in progress | Model property changed; system serializes to temporary SQLite, wraps in FileWrapper, and writes to package |
| Session restoration | App launches; previously open document URLs are reopened; any that fail are logged and skipped |

## Accessibility

Not applicable — this recipe defines a storage and persistence pattern with no direct user interface. Document open/save/error dialogs inherit platform-standard accessibility from `NSSavePanel`, `NSOpenPanel`, and SwiftUI alert presentations.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pd-001 | package-uttype-declaration, unique-file-extension, swift-uttype-property | Register UTType for `.catnip-proj` conforming to `com.apple.package` | Finder displays the package directory as a single file icon with the correct extension |
| pd-002 | reference-file-document, published-model-property | Create a new `ProjectDocument` and modify the `model` property | `objectWillChange` fires; auto-save triggers |
| pd-003 | filewrapper-read-write | Call `fileWrapper(snapshot:configuration:)` on a document | Returns a `FileWrapper` of kind directory containing `project.db` |
| pd-004 | journal-mode-off | Open the SQLite database inside a saved package | `PRAGMA journal_mode` returns `off` |
| pd-005 | pragma-user-version, metadata-table | Open the SQLite database and query `PRAGMA user_version` and `SELECT * FROM metadata` | `user_version` matches expected schema version; metadata row contains name, version, created_date |
| pd-006 | settings-table, boolean-string-storage, numeric-string-storage | Insert boolean setting `autoSave = true` and numeric setting `fontSize = 14` | Settings table contains `("autoSave", "true")` and `("fontSize", "14")` |
| pd-007 | check-sqlite-first | Open a package containing `project.db` | Document reads from SQLite successfully |
| pd-008 | fallback-legacy-json, deserialize-legacy-json | Open a package containing `data.json` but no `project.db` | Document reads from JSON; model is populated correctly |
| pd-009 | deserialize-legacy-json | Open a legacy JSON package, modify model, trigger save | Saved package contains `project.db` (SQLite); legacy JSON format replaced |
| pd-010 | empty-package-defaults | Open an empty package directory (no `project.db`, no `data.json`) | Document initializes with default values |
| pd-011 | log-format-version | Open a SQLite document with schema version 3 | Log entry: `info` level, includes "schema version 3" |
| pd-012 | temp-sqlite-write, parameterized-queries, read-temp-bytes | Trigger a save on a document with model data | Temporary SQLite file is created, data is inserted with parameterized queries, bytes are read |
| pd-013 | wrap-database-filewrapper, directory-filewrapper | Inspect the FileWrapper returned from `fileWrapper(...)` | Directory FileWrapper with one child whose `preferredFilename` is `project.db` |
| pd-014 | cleanup-temp-database | Trigger a save and inspect the temporary directory afterward | No leftover temporary `.db` files remain |
| pd-015 | migration-safe-codable, backward-compatible-schema | Deserialize a legacy JSON document that is missing a field added in a newer schema version | Missing field falls back to its default value; no crash or error |
| pd-016 | migration-safe-codable, backward-compatible-schema | Deserialize a legacy JSON document that contains an unknown extra field | Extra field is ignored; known fields are populated correctly |
| pd-017 | model-version-field | Inspect the model after reading from either JSON or SQLite | Model's `version` field is populated and matches the source's schema version |
| pd-018 | temp-database-url-helper | Call `tempDatabaseURL()` twice | Both URLs are in the temp directory, have `.db` extension, and are unique (different UUIDs) |
| pd-019 | exec-with-bindings | Call `exec("INSERT INTO settings (key, value) VALUES (?, ?)", [.text("k"), .text("v")])` | Row is inserted; no SQL injection possible with parameterized bindings |
| pd-020 | query-functions | Call `queryRow("SELECT value FROM settings WHERE key = ?", [.text("k")])` | Returns single row with value `"v"` |
| pd-021 | last-insert-row-id | Insert a row and call `lastInsertRowID()` | Returns the integer row ID of the just-inserted row |
| pd-022 | sqlite-error-type | Attempt to open a non-existent database path | Throws error of type `.cannotOpen` |
| pd-023 | sqlite-error-type | Execute invalid SQL | Throws error of type `.execFailed` |
| pd-024 | document-group-scene | Launch the app | `DocumentGroup` scenes are registered for each document type; File > Open shows the correct file type filters |
| pd-025 | autosave-via-published | Modify the model's `@Published` property | Auto-save fires without any user action |
| pd-026 | save-open-urls-on-quit | Open two documents, quit the app | Both document URLs are saved for session restoration |
| pd-027 | restore-urls-on-launch | Launch the app after quitting with two documents open | Both documents reopen; if one URL is invalid, the valid one still opens and the failure is logged |

## Edge Cases

- **Corrupt SQLite database**: If `sqlite3_open` succeeds but queries fail (e.g., malformed schema, incomplete write), the document MUST surface a user-facing error describing the corruption and MUST NOT overwrite the corrupt file. The user should be offered the option to create a new document or attempt manual recovery.
- **Missing files in package**: If the package directory exists but contains neither the expected SQLite database nor a legacy JSON file, the document treats this as a new empty document (empty-package-defaults). If the package directory itself is missing or inaccessible, the system reports a file-not-found error.
- **Format migration (JSON to SQLite)**: When a legacy JSON document is opened, the model is populated from JSON. On the next save, the write process creates a SQLite database. The legacy JSON file is not explicitly deleted from the package — the new `FileWrapper(directoryWithFileWrappers:)` simply omits it, and the atomic directory replacement removes it.
- **Concurrent access**: If two processes or two app instances attempt to open the same package document simultaneously, behavior is undefined. The pattern relies on macOS file coordination (`NSFileCoordinator`) when available, but does not implement custom locking. Documents opened via `DocumentGroup` benefit from the system's built-in file coordination.
- **Disk full during write**: If the temporary SQLite file cannot be fully written due to insufficient disk space, the `exec()` call will fail. The document MUST catch this error and surface it to the user. The existing on-disk package MUST NOT be modified or corrupted.
- **Very large documents**: For documents with tens of thousands of rows, the write process creates the entire database in memory (temporary file). If memory pressure is a concern, the implementation SHOULD write incrementally and monitor for memory warnings on iOS.
- **Schema downgrade attempt**: If a document's `user_version` is higher than the app's current schema version, the document MUST refuse to load and present an error indicating that a newer version of the app is required (see States table).
- **Temporary file cleanup failure**: If the temporary database file cannot be deleted after reading its bytes, the operation SHOULD still succeed (the data was already captured). The leftover temp file will be cleaned up by the OS eventually.
- **Package opened by external tool**: If a user right-clicks "Show Package Contents" and modifies the SQLite database externally, the app has no mechanism to detect this. The next open will read whatever state the database is in. No integrity checking beyond schema version is performed.
- **Empty settings table**: If the settings table exists but contains no rows, all settings MUST fall back to their coded default values. This is not an error condition.
- **Date parsing failures**: If a date string in the metadata table does not conform to ISO 8601, the `invalidDate` error MUST be thrown and surfaced, rather than silently using a fallback date.
- **Multiple database files in package**: If future versions add additional database files to the package (e.g., `cache.db`), the read/write process MUST handle the presence of unknown files gracefully — they are preserved in the directory FileWrapper during write.

## Logging

Subsystem: `{{bundle_id}}` | Category: `PackageDocument`

| Event | Level | Message |
|-------|-------|---------|
| Document opened (SQLite) | info | `PackageDocument: opened "{{filename}}" (SQLite schema version {{version}})` |
| Document opened (legacy JSON) | info | `PackageDocument: opened "{{filename}}" (legacy JSON format)` |
| Document opened (empty package) | info | `PackageDocument: opened "{{filename}}" (empty package, defaults applied)` |
| Document created | info | `PackageDocument: created new document "{{filename}}"` |
| Write started | debug | `PackageDocument: write started for "{{filename}}"` |
| Temp database created | debug | `PackageDocument: temp database created at "{{tempPath}}"` |
| Data inserted | debug | `PackageDocument: inserted {{rowCount}} rows into {{tableName}}` |
| Temp database bytes read | debug | `PackageDocument: read {{byteCount}} bytes from temp database` |
| Temp database cleaned up | debug | `PackageDocument: temp database deleted at "{{tempPath}}"` |
| Write completed | debug | `PackageDocument: write completed for "{{filename}}"` |
| Legacy migration triggered | info | `PackageDocument: migrating "{{filename}}" from legacy JSON to SQLite` |
| Schema migration triggered | info | `PackageDocument: migrating "{{filename}}" from schema version {{oldVersion}} to {{newVersion}}` |
| Session URLs saved | debug | `PackageDocument: saved {{count}} open document URLs for session restoration` |
| Session restoration started | info | `PackageDocument: restoring {{count}} documents from previous session` |
| Session restoration failed for URL | warning | `PackageDocument: failed to restore document at "{{url}}": {{error}}` |
| Corrupt database detected | error | `PackageDocument: corrupt database in "{{filename}}": {{error}}` |
| Schema version too new | error | `PackageDocument: "{{filename}}" has schema version {{version}}, app supports up to {{maxVersion}}` |
| Disk full during write | error | `PackageDocument: write failed for "{{filename}}": disk full or I/O error: {{error}}` |
| SQLite open failed | error | `PackageDocument: cannot open database at "{{path}}": {{error}}` |
| SQL exec failed | error | `PackageDocument: exec failed: {{sql}} — {{error}}` |
| Temp file cleanup failed | warning | `PackageDocument: failed to delete temp database at "{{tempPath}}": {{error}}` |
| Date parsing failed | error | `PackageDocument: invalid date string "{{dateString}}" in metadata table` |

## Platform Notes

- **macOS (SwiftUI)**: Use `ReferenceFileDocument` with `DocumentGroup(newDocument:)` for each document type. The `@Published var model` pattern drives auto-save through `objectWillChange`. For file creation outside the standard `DocumentGroup` flow (e.g., "New Project" menu items), use `NSSavePanel` to choose a location and then programmatically create the package directory and initial database. `NSWorkspace` file coordination applies automatically to `DocumentGroup`-managed documents. UTType declarations go in the target's Info.plist under `UTExportedTypeDeclarations`. Use `FileWrapper(directoryWithFileWrappers:)` for the package and `FileWrapper(regularFileWithContents:)` for each file inside it.
- **macOS (AppKit)**: Use `NSDocument` subclass with `override class var readableTypes` and `override class var writableTypes`. Override `read(from:ofType:)` and `fileWrapper(ofType:)` with the same SQLite read/write logic. `NSDocument` provides auto-save for free when `autosavesInPlace` returns `true`. Package document support is enabled by returning `true` from `class var isNativeType(_:)` for the custom UTType.
- **iOS**: `ReferenceFileDocument` works on iOS with `DocumentGroup`. The package is stored in the app's container or iCloud Drive. File coordination is handled by the system. `NSSavePanel` and `NSOpenPanel` are not available — use `.fileImporter()` and `.fileExporter()` modifiers instead. The same SQLite read/write logic applies. Note that iOS sandboxing requires security-scoped URL access for user-selected documents.
- **visionOS**: Same as iOS. `DocumentGroup` renders document management UI in the visionOS window style. No platform-specific changes to the storage layer.

## Design Decisions

**Document creation flows are in `menu-commands.md`**: This spec covers the read/write/migration lifecycle of package documents. The "New Project" and "New Workspace" creation flows (NSOpenPanel, git validation, NSSavePanel) are documented in `ui/Recipes/menu-commands.md` since they involve menu command structure and file picker UX, not just persistence.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

<!-- leaf: recipes-infrastructure/package-document · source: recipes/infrastructure/package-document.md -->

**Rules** (cite as `recipes-infrastructure/package-document#<slug>`):

- `package-uttype-declaration` MUST
- `unique-file-extension` MUST
- `swift-uttype-property` MUST
- `reference-file-document` MUST
- `published-model-property` MUST
- `filewrapper-read-write` MUST
- `journal-mode-off` MUST
- `pragma-user-version` MUST
- `metadata-table` MUST
- `settings-table` MUST
- `boolean-string-storage` MUST
- `numeric-string-storage` MUST
- `domain-specific-tables` MUST
- `check-sqlite-first` MUST
- `fallback-legacy-json` MUST
- `deserialize-legacy-json` MUST
- `empty-package-defaults` MUST
- `log-format-version` MUST
- `temp-sqlite-write` MUST
- `parameterized-queries` MUST
- `read-temp-bytes` MUST
- `wrap-database-filewrapper` MUST
- `directory-filewrapper` MUST
- `cleanup-temp-database` MUST
- `migration-safe-codable` MUST
- `model-version-field` MUST
- `backward-compatible-schema` MUST
- `temp-database-url-helper` MUST
- `exec-with-bindings` MUST
- `query-functions` MUST
- `last-insert-row-id` MUST
- `sqlite-error-type` MUST
- `document-group-scene` MUST
- `non-document-window-group` MUST
- `custom-menu-save-panel` MUST
- `autosave-via-published` MUST
- `save-open-urls-on-quit` MUST
- `restore-urls-on-launch` MUST

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


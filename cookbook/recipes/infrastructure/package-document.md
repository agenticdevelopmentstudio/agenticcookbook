---
id: b2ba3ab9-743f-4c86-a75f-cc2e93fd3b07
title: "Package Document"
domain: agenticdevelopercookbook://recipes/infrastructure/package-document
type: recipe
version: 2.0.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
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
ingredients:
  - agenticdevelopercookbook://ingredients/infrastructure/package-document-type
  - agenticdevelopercookbook://ingredients/infrastructure/package-document-storage
  - agenticdevelopercookbook://ingredients/infrastructure/sqlite-helpers
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Package Document

## Overview

A pattern for macOS document-based apps that use directory bundle packages (rendered as single files in Finder) containing SQLite databases. The document is a folder with a custom UTType conforming to `com.apple.package`, registered with a file extension (e.g., `.catnip-proj`, `.catnip-workspace`). Inside the package, one or more SQLite database files store all persistent state. The pattern supports schema versioning via `PRAGMA user_version`, format migration from legacy JSON files to SQLite, atomic writes through temporary database creation and `FileWrapper` packaging, and auto-save via SwiftUI's `ReferenceFileDocument` protocol. Each document type (project, workspace) follows the same structural pattern with its own UTType, file extension, database filename, and schema.

The recipe composes three ingredients. The package document type registers the UTType and owns the document protocol conformance, scenes, and lifecycle. The package document storage owns what is inside the package and the read, write, and migration process. The SQLite helpers are the safe database layer the storage format uses.

### Terminology

The terms Package document, UTType, ReferenceFileDocument, FileWrapper, and Document scene are defined in the package document type ingredient. The terms Schema version, Format migration, Atomic write, and Key-value settings are defined in the package document storage ingredient.

### Architecture

The architecture diagram of the document, auto-save path, and package on disk is in the package document storage ingredient. In this recipe the same flow is split across the three ingredients as shown in [Layout](#layout).

### Logging

Logging is specified per ingredient under subsystem `{{bundle_id}}` and category `PackageDocument`. Document created and session restoration events are in the package document type ingredient; open, write, migration, corruption, disk-full, date-parsing, and temp-file events are in the package document storage ingredient; SQLite open and exec failures are in the SQLite helpers ingredient.

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Package document type | `agenticdevelopercookbook://ingredients/infrastructure/package-document-type` | Registers the UTType, conforms the document class to `ReferenceFileDocument`, declares the `DocumentGroup` scenes, and owns auto-save and session restoration | Yes | One instance per document kind: UTType identifier, file extension, document class |
| Package document storage | `agenticdevelopercookbook://ingredients/infrastructure/package-document-storage` | Defines the package contents, the SQLite schema, the read process with legacy JSON fallback, the atomic write process, and migration-safe Codable | Yes | Database filename, legacy JSON filename, current schema version, and domain-specific tables per document kind |
| SQLite helpers | `agenticdevelopercookbook://ingredients/infrastructure/sqlite-helpers` | Parameterized execution, row queries, temporary database URL, and the SQLite error type | Yes | None |

## Integration Requirements

- **document-delegates-to-storage**: The document class declared by the package document type MUST implement `init(configuration:)` by running the storage read process and `fileWrapper(snapshot:configuration:)` by running the storage write process. The document class MUST NOT contain its own SQLite or JSON handling.
- **storage-uses-sqlite-helpers**: The storage read and write processes MUST access SQLite only through the SQLite helpers, passing every value as a binding. The storage MUST NOT call the `sqlite3` API directly or build SQL by string interpolation.
- **autosave-ends-in-atomic-replacement**: An auto-save triggered by the `@Published` model MUST result in a temporary database write, a byte read, and a directory `FileWrapper` handed back to the document system, so the package on disk is replaced as a whole and never partially written.
- **restoration-uses-storage-read**: Documents reopened during session restoration MUST be read through the same storage read process, including the legacy JSON fallback and schema version check, as documents opened by the user.
- **errors-surface-through-document**: A `SQLiteError` raised by the helpers, a corrupt database, or a schema version newer than the app supports MUST surface to the user through the document open or save error path, and MUST leave the existing package on disk unmodified.
- **shared-log-category**: All three ingredients MUST log under the single `PackageDocument` category so one filter shows a document's complete lifecycle.
- **unique-database-name-per-kind**: Each document kind MUST use its own UTType, file extension, and database filename; two kinds MUST NOT share an extension.

## Layout

This is a non-UI recipe, so the layout is the layering of the components and the direction of the data flow. Calls go downward; nothing below imports from above.

```
 Finder / File > Open / session restoration
            │
 ┌──────────▼──────────────────────────────────────────┐
 │ Package document type                                │
 │  UTType (com.apple.package) · DocumentGroup scenes   │
 │  ReferenceFileDocument · @Published model → autosave │
 └──────────┬──────────────────────────────────────────┘
            │ init(configuration:)  /  fileWrapper(snapshot:configuration:)
 ┌──────────▼──────────────────────────────────────────┐
 │ Package document storage                             │
 │  read: project.db → legacy JSON → empty defaults     │
 │  write: temp SQLite → bytes → FileWrapper(directory) │
 └──────────┬──────────────────────────────────────────┘
            │ exec / queryRow / queryAll / lastInsertRowID
 ┌──────────▼──────────────────────────────────────────┐
 │ SQLite helpers  (bindings only · SQLiteError)        │
 └─────────────────────────────────────────────────────┘

 Package on disk:   MyDocument.catnip-proj/   project.db   (legacy: data.json)
```

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| Document model | Package document storage (on read) and the UI (edits) | Package document type, the UI | two-way | `@Published var model` on the document; each change fires `objectWillChange` |
| Model snapshot | Package document type | Package document storage write process | one-way | The snapshot passed to `fileWrapper(snapshot:configuration:)` |
| Package `FileWrapper` | Package document storage | Document system | one-way | Directory `FileWrapper` containing the database file wrapper, replaced atomically |
| Schema version | `PRAGMA user_version` in the database | Package document storage | one-way | Read on open and compared with the app's current version |
| Open document URLs | Package document type | Session restoration on next launch | one-way | Saved on quit, reopened on launch, failures logged and skipped |
| Temporary database path | SQLite helpers (`tempDatabaseURL()`) | Package document storage write process | one-way | UUID-named file in the temporary directory, deleted after its bytes are read |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pd-028 | document-delegates-to-storage, autosave-ends-in-atomic-replacement | Modify the `@Published` model of an open document | Auto-save runs the storage write process; the document returns a directory `FileWrapper` with one child `project.db`; no temporary `.db` file remains |
| pd-029 | storage-uses-sqlite-helpers | Save a document whose model contains a string with an SQL metacharacter such as `'; DROP TABLE settings; --` | The value is stored verbatim through a binding; the settings table still exists |
| pd-030 | document-delegates-to-storage, restoration-uses-storage-read | Quit with a legacy-JSON document open (no `project.db`), relaunch | The document reopens through the storage read process with the model populated from JSON; the next save writes SQLite |
| pd-031 | errors-surface-through-document | Open a package whose `project.db` is corrupt | The user sees an error; the file on disk is not modified; other restored documents still open |
| pd-032 | errors-surface-through-document | Open a package whose `user_version` is higher than the app's schema version | The document refuses to load and reports that a newer app version is required |
| pd-033 | unique-database-name-per-kind | Register a project kind and a workspace kind | Each has its own UTType, extension, and database filename |

Vectors pd-001 to pd-027 are single-ingredient vectors and appear in the ingredients under new IDs: the package document type holds pd-001, pd-002, pd-003, pd-024, pd-025, pd-026, and pd-027 (as pd-type-001 to pd-type-008, which add a non-document-window-group vector); the package document storage holds pd-004 to pd-017 (as pd-store-001 to pd-store-015, which add a domain-specific-tables vector); and the SQLite helpers hold pd-018 to pd-023 (as sqlite-helpers-001 to sqlite-helpers-007, which add a `queryAll` vector).

## Edge Cases

- **Corrupt SQLite database across the composition**: If `sqlite3_open` succeeds but queries fail, the helpers raise an error, the storage read process stops, and the document surfaces the failure. The corrupt file MUST NOT be overwritten (errors-surface-through-document).
- **Format migration (JSON to SQLite)**: When a legacy JSON document is opened, the model is populated from JSON. On the next save, the write process creates a SQLite database. The legacy JSON file is not explicitly deleted from the package — the new `FileWrapper(directoryWithFileWrappers:)` simply omits it, and the atomic directory replacement removes it.
- **Concurrent access**: If two processes or two app instances attempt to open the same package document simultaneously, behavior is undefined. The pattern relies on macOS file coordination (`NSFileCoordinator`) when available, but does not implement custom locking. Documents opened via `DocumentGroup` benefit from the system's built-in file coordination.
- **Disk full during write**: If the temporary SQLite file cannot be fully written due to insufficient disk space, the `exec()` call will fail. The document MUST catch this error and surface it to the user. The existing on-disk package MUST NOT be modified or corrupted.
- **Very large documents**: For documents with tens of thousands of rows, the write process creates the entire database in memory (temporary file). If memory pressure is a concern, the implementation SHOULD write incrementally and monitor for memory warnings on iOS.
- **Schema downgrade attempt**: If a document's `user_version` is higher than the app's current schema version, the document MUST refuse to load and present an error indicating that a newer version of the app is required.
- **Temporary file cleanup failure**: If the temporary database file cannot be deleted after reading its bytes, the operation SHOULD still succeed (the data was already captured). The leftover temp file will be cleaned up by the OS eventually.
- **Package opened by external tool**: If a user right-clicks "Show Package Contents" and modifies the SQLite database externally, the app has no mechanism to detect this. The next open will read whatever state the database is in. No integrity checking beyond schema version is performed.
- **Empty settings table**: If the settings table exists but contains no rows, all settings MUST fall back to their coded default values. This is not an error condition.
- **Date parsing failures**: If a date string in the metadata table does not conform to ISO 8601, the `invalidDate` error MUST be thrown and surfaced, rather than silently using a fallback date.
- **Multiple database files in package**: If future versions add additional database files to the package (e.g., `cache.db`), the read/write process MUST handle the presence of unknown files gracefully — they are preserved in the directory FileWrapper during write.
- **Invalid URL at restoration**: A saved URL that no longer exists is logged and skipped; it MUST NOT prevent other documents from reopening.

## Platform Notes

- **SwiftUI (macOS)**: Use `ReferenceFileDocument` with `DocumentGroup(newDocument:)` for each document type. The `@Published var model` pattern drives auto-save through `objectWillChange`. For file creation outside the standard `DocumentGroup` flow (e.g., "New Project" menu items), use `NSSavePanel` to choose a location and then programmatically create the package directory and initial database. `NSWorkspace` file coordination applies automatically to `DocumentGroup`-managed documents. UTType declarations go in the target's Info.plist under `UTExportedTypeDeclarations`. Use `FileWrapper(directoryWithFileWrappers:)` for the package and `FileWrapper(regularFileWithContents:)` for each file inside it.
- **macOS (AppKit)**: Use `NSDocument` subclass with `override class var readableTypes` and `override class var writableTypes`. Override `read(from:ofType:)` and `fileWrapper(ofType:)` with the same SQLite read/write logic. `NSDocument` provides auto-save for free when `autosavesInPlace` returns `true`. Package document support is enabled by returning `true` from `class var isNativeType(_:)` for the custom UTType.
- **iOS**: `ReferenceFileDocument` works on iOS with `DocumentGroup`. The package is stored in the app's container or iCloud Drive. File coordination is handled by the system. `NSSavePanel` and `NSOpenPanel` are not available — use `.fileImporter()` and `.fileExporter()` modifiers instead. The same SQLite read/write logic applies. Note that iOS sandboxing requires security-scoped URL access for user-selected documents.
- **visionOS**: Same as iOS. `DocumentGroup` renders document management UI in the visionOS window style. No platform-specific changes to the storage layer.
- **Windows**: The package is an ordinary directory containing a SQLite file; the same schema, versioning, and temp-file-then-replace write apply, using the platform's atomic rename.
- **Compose / React/Web**: Not applicable — UTType, `DocumentGroup`, and `FileWrapper` are Apple frameworks. The storage and SQLite helper requirements apply to any runtime with a SQLite binding.

## Design Decisions

**Decision**: Document creation flows are in `menu-commands.md`, not in this recipe.
**Rationale**: This spec covers the read/write/migration lifecycle of package documents. The "New Project" and "New Workspace" creation flows (NSOpenPanel, git validation, NSSavePanel) are specified by the Document Creation Flow ingredient (`agenticdevelopercookbook://ingredients/app/document-creation-flow`), composed by the Menu Commands recipe, since they involve menu command structure and file picker UX, not just persistence.
**Approved**: pending

**Decision**: Split the pattern into a document type, a storage format, and a SQLite helper layer.
**Rationale**: The helpers are reusable by any code that touches SQLite, the storage format varies per document kind while the document type scaffolding repeats, and each layer can change without touching the others.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [data-integrity](agenticdevelopercookbook://compliance/reliability#data-integrity) | partial | Reliability |
| [state-recovery](agenticdevelopercookbook://compliance/reliability#state-recovery) | partial | Reliability |
| [input-sanitization](agenticdevelopercookbook://compliance/security#input-sanitization) | partial | Security |

> Status is `partial`: this recipe specifies the integration-level requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.1 | 2026-10-04 | Mike Fullerton | Point creation flows at the document-creation-flow ingredient |
| 2.0.0 | 2026-10-04 | Mike Fullerton | Restructure into recipe shape; extract component behavior into ingredients |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

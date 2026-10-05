---
id: CF2B27B3-199E-4779-AC15-7923A9FEFC1F
title: "Workspace Document"
domain: agenticdevelopercookbook://ingredients/ui/windows/workspace-document
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "SQLite-backed workspace package of project and directory entries with a pooled directory-watch manager, discovery, and entry validation"
platforms:
  - macos
  - swift
  - web
tags:
  - document
  - sqlite
  - workspace
depends-on: []
related:
  - agenticdevelopercookbook://ingredients/ui/windows/workspace-browser
  - agenticdevelopercookbook://recipes/ui/windows/workspace-window
  - agenticdevelopercookbook://recipes/infrastructure/directory-sync
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Workspace Document

## Overview

The persisted workspace model and the directory-watching pool behind it. A workspace is a `.catnip-workspace` package containing a `workspace.db` SQLite database of entries (project and directory references), auto-discovered projects, and settings. A `WorkspaceDirectoryManager` owns one `DirectoryWatchCoordinator` per directory entry, aggregates their sync state, and reports discovered `.catnip-proj` packages. Entry validation prevents duplicates and self-reference. This ingredient has no visual presentation; terms such as Workspace, Entry, and Discovered project are defined in the Workspace Browser ingredient's Terminology.

## Behavioral Requirements

### Workspace Document

- **workspace-package-format**: The workspace MUST be stored as a `.catnip-workspace` package (directory) containing a `workspace.db` SQLite database.
- **sqlite-table-schema**: The SQLite database MUST contain the following tables:
  - `workspace` — metadata (name, creation date, last modified date)
  - `entries` — project and directory references (id, type, path, name, date added)
  - `discovered_projects` — auto-found `.catnip-proj` packages (id, entry_id, path, name)
  - `settings` — key-value settings (key, value), including `sidebarProportion`
- **sync-on-entry-change**: Adding or removing an entry MUST update the workspace document, which MUST trigger `syncEntries` to reconcile the `WorkspaceDirectoryManager` coordinator pool.

### Workspace Directory Manager

- **coordinator-pool-manager**: The `WorkspaceDirectoryManager` MUST manage a pool of `DirectoryWatchCoordinator` instances, one per directory entry, as specified in [directory-sync.md](../../../recipes/infrastructure/directory-sync.md) coordinator-per-entry through dedicated-cache-directory.
- **aggregate-sync-state**: The manager MUST aggregate `isSyncing` across all coordinators. The workspace-level `isSyncing` MUST be `true` if any coordinator is syncing.
- **auto-discover-projects**: The manager MUST auto-discover `.catnip-proj` packages within each watched directory and report them via an `onDiscoveryChanged` callback for document persistence.
- **per-entry-cache-dir**: Each coordinator MUST use a dedicated cache directory named `cache-{entryID}` within the workspace package.

### Entry Types and Validation

- **entry-type-enum**: Entry type MUST be one of: `.project` (direct reference to a `.catnip-proj` file) or `.directory` (a directory scanned for projects).
- **auto-correct-entry-type**: If an entry has type `.project` but its path does not end with `.catnip-proj`, the type MUST be automatically corrected to `.directory` (entry type migration).
- **prevent-self-referential**: The workspace MUST prevent adding its own `.catnip-workspace` package as an entry (self-referential loop detection). If the user attempts to add a path that resolves to the workspace's own package, the add operation MUST be rejected and a warning MUST be logged.
- **prevent-duplicate-entry**: The workspace MUST prevent adding duplicate entries. If the user attempts to add a path already present as an entry, the add operation MUST be rejected.

## Appearance

Not applicable: this ingredient is a data model and watcher pool with no visual presentation; the Workspace Browser ingredient renders it.

## States

| State | Behavior |
|-------|----------|
| Entry removed | Entry disappears from sidebar, coordinator stopped (if directory), document updated |
| Entry added | Entry appears in sidebar, coordinator started (if directory), document updated |
| Self-referential add rejected | Add operation silently rejected, warning logged (prevent-self-referential) |
| Entry type migrated | Entry with incorrect type auto-corrected on load (auto-correct-entry-type) |

## Accessibility

Not applicable: this ingredient has no user interface; accessibility of the entries it supplies is specified by the Workspace Browser ingredient.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| ws-018 | workspace-package-format, sqlite-table-schema | Inspect workspace package on disk | `.catnip-workspace` directory contains `workspace.db` with tables: workspace, entries, discovered_projects, settings |
| ws-019 | sync-on-entry-change | Add a directory entry via UI | Entry appears in `entries` table, `syncEntries` fires, new coordinator created |
| ws-020 | sync-on-entry-change | Remove a directory entry via context menu | Entry removed from `entries` table, coordinator stopped and removed |
| ws-021 | coordinator-pool-manager | Workspace with 3 directory entries | WorkspaceDirectoryManager has 3 coordinators |
| ws-022 | aggregate-sync-state | 1 of 3 coordinators syncing | Workspace-level `isSyncing` is `true` |
| ws-023 | aggregate-sync-state | All 3 coordinators idle | Workspace-level `isSyncing` is `false` |
| ws-024 | auto-discover-projects | Directory entry contains a new `.catnip-proj` package | `onDiscoveryChanged` fires, `discovered_projects` table updated |
| ws-025 | per-entry-cache-dir | Workspace with entry ID "abc" | Cache directory is `cache-abc` within workspace package |
| ws-026 | auto-correct-entry-type | Entry has type `.project` but path is `/Users/me/Code` (no `.catnip-proj` suffix) | Type auto-corrected to `.directory` |
| ws-027 | prevent-self-referential | Attempt to add workspace's own `.catnip-workspace` path as an entry | Add rejected, warning logged |
| ws-028 | prevent-duplicate-entry | Attempt to add `/Users/me/Code` when it already exists as an entry | Add rejected |

## Edge Cases

- **Self-referential add**: prevent-self-referential prevents it. The check MUST resolve symlinks and normalize paths before comparison.
- **Duplicate path add**: prevent-duplicate-entry prevents it. Paths MUST be compared after normalization (resolve symlinks, remove trailing slashes).
- **Rapid add/remove**: Document writes MUST be serialized to prevent SQLite contention. `syncEntries` MUST handle the coordinator pool converging to the current entry list without race conditions.
- **Workspace file locked or read-only**: Document operations MUST fail gracefully with a user-visible error. The UI MUST NOT crash.
- **Entry type migration on load**: If the workspace database contains entries with incorrect types (auto-correct-entry-type), migration MUST happen silently on load without user intervention.
- **Workspace package corruption**: If `workspace.db` is missing or corrupt within the `.catnip-workspace` package, the document SHOULD attempt to recreate the database with empty tables. A warning MUST be logged.
- **Concurrent workspace access**: If the same workspace is opened in two app instances, SQLite WAL mode SHOULD handle concurrent reads. Writes from one instance SHOULD NOT corrupt the other's state.

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `sidebarProportion` | `Double` | `0.3` | Persisted in the `settings` table; sidebar width as a fraction of window width |
| `cacheDirectoryName` | string pattern | `cache-{entryID}` | Per-entry cache directory inside the workspace package |
| `journalMode` | enum | WAL | SQLite journal mode for concurrent read safety |

## Privacy

- **Data collected**: Workspace entry paths and project names, stored locally in `workspace.db`.
- **Storage**: A `.catnip-workspace` package on the user's disk; no data is stored elsewhere.
- **Transmission**: None — workspace data never leaves the device.
- **Retention**: Until the user removes the entry or deletes the workspace package.

## Logging

Subsystem: `{{bundle_id}}` | Category: `WorkspaceWindow`

| Event | Level | Message |
|-------|-------|---------|
| Entry added | info | `WorkspaceWindow: added {{entryType}} entry "{{path}}"` |
| Entry removed | info | `WorkspaceWindow: removed {{entryType}} entry "{{path}}"` |
| Entry type migrated | warning | `WorkspaceWindow: migrated entry "{{path}}" from .project to .directory (path does not end with .catnip-proj)` |
| Self-referential add rejected | warning | `WorkspaceWindow: rejected self-referential add of "{{path}}"` |
| Duplicate add rejected | warning | `WorkspaceWindow: rejected duplicate entry "{{path}}"` |
| Discovery changed | debug | `WorkspaceWindow: discovery changed for entry "{{entryID}}", {{count}} projects found` |
| Sync entries triggered | debug | `WorkspaceWindow: syncEntries triggered, {{entryCount}} entries` |
| Coordinator created | debug | `WorkspaceWindow: coordinator created for entry "{{entryID}}"` |
| Coordinator removed | debug | `WorkspaceWindow: coordinator removed for entry "{{entryID}}"` |
| Workspace DB opened | debug | `WorkspaceWindow: database opened at "{{dbPath}}"` |
| Workspace DB error | error | `WorkspaceWindow: database error: {{error}}` |
| Workspace DB recreated | warning | `WorkspaceWindow: database recreated due to corruption` |

## Platform Notes

- **SwiftUI (macOS)**: `WorkspaceDirectoryManager` is `@Observable` (or `ObservableObject`) with `@Published isSyncing`. SQLite access via direct `sqlite3` C API or a lightweight Swift wrapper. Use WAL mode for concurrent read safety. Sidebar proportion persisted in the workspace SQLite `settings` table.
- **visionOS**: Same implementation as macOS; the data layer has no platform-specific differences.
- **Compose**: Use a `StateFlow<Boolean>` for aggregated `isSyncing` and an SQLite binding (Room or SQLDelight) for the workspace database.
- **React/Web**: The package format maps to a directory-handle-based store; use an in-browser SQLite build or IndexedDB with the same logical tables.

## Design Decisions

**Decision**: The workspace is a package directory containing a SQLite database rather than a single flat file.
**Rationale**: A package allows per-entry cache directories to live beside the database and keeps the document atomic from the user's viewpoint.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [privacy](agenticdevelopercookbook://guidelines/implementing/security/privacy) | partial | Privacy |
| [error-responses](agenticdevelopercookbook://guidelines/implementing/networking/error-responses) | partial | Best Practices |
| [lifecycle-patterns](agenticdevelopercookbook://guidelines/planning/code-quality/lifecycle-patterns) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Workspace Window recipe |

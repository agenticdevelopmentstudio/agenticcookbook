---
id: 7C689B1F-37DB-4422-A129-270C697D5875
title: "Directory Tree Cache"
domain: agenticdevelopercookbook://ingredients/infrastructure/directory-tree-cache
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "On-disk JSON cache of a flattened file tree, loaded off the main thread for instant display and written atomically"
platforms:
  - ios
  - macos
  - swift
  - typescript
tags:
  - directory-sync
  - infrastructure
  - cache
depends-on: []
related:
  - agenticdevelopercookbook://recipes/infrastructure/directory-sync
  - agenticdevelopercookbook://ingredients/infrastructure/directory-watch-coordinator
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Directory Tree Cache

## Overview

A directory tree cache persists an in-memory file tree to a JSON file so the next launch can show a tree instantly, before any filesystem scan has finished. The tree is stored as a flattened array of entries whose parent-child relationships are rebuilt on load, and every write is atomic so an interrupted write can never leave a corrupt cache. Use it wherever a UI shows a potentially large directory tree and must not wait for a scan to display something.

### Terminology

| Term | Definition |
|------|-----------|
| Cache | A JSON file (`file-tree-cache.json`) containing a flattened array of `FileTreeCacheEntry` values |
| File tree node | An in-memory representation of a single file or directory: path, name, metadata, and children |

## Behavioral Requirements

### Load

- **load-cached-tree**: On startup, the cache loader MUST attempt to load a cached tree from the JSON file `file-tree-cache.json` for instant display.
- **background-cache-load**: The cache MUST be loaded synchronously on a background queue so the main thread is never blocked.
- **handle-missing-cache**: If no cache file exists or the file cannot be read, the loader MUST present an empty or loading state. It MUST NOT crash or block.

### Format

- **json-cache-format**: The cache MUST be stored as a JSON file using the following entry structure:
  ```
  FileTreeCacheEntry {
    path: String
    parentPath: String?   // nil for root
    name: String
    isDirectory: Bool
    isPackage: Bool
    fileSize: Int?
    modificationDate: Date?   // ISO 8601 encoded
  }
  ```
- **flattened-cache-array**: The cache MUST be a flattened array of `FileTreeCacheEntry` values. Parent-child relationships MUST be reconstructed from `path` / `parentPath` on load.
- **atomic-cache-writes**: Cache writes MUST be atomic — write to a temporary file first, then rename into place. This prevents corruption from interrupted writes.

### Save

- **cache-save-nonblocking**: A cache save MUST be a fire-and-forget operation on a background queue. A save failure MUST NOT block or crash the caller.

## Appearance

Not applicable — a cache is infrastructure with no visual surface.

## States

| State | Behavior |
|-------|----------|
| No cache | Loader returns an empty state; the caller begins a full sync immediately |
| Cache loaded | Entries are reconstructed into a tree and handed to the caller for display |
| Cache corrupt or unreadable | Treated exactly like no cache; a warning is logged |
| Saving | A background write to a temporary file is in progress |
| Saved | The temporary file has been atomically renamed over the cache file |

## Accessibility

Not applicable — a cache has no user-facing surface. Presentation of the tree is handled by the file-tree-browser ingredient.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| tree-cache-001 | load-cached-tree, background-cache-load | Launch with a valid `file-tree-cache.json` on disk | Cached tree is loaded on a background queue and returned without blocking the main thread |
| tree-cache-002 | handle-missing-cache | Launch with no cache file on disk | Empty/loading state is returned; no error |
| tree-cache-003 | handle-missing-cache | Launch with a corrupt (invalid JSON) cache file | Empty/loading state is returned; no error |
| tree-cache-004 | atomic-cache-writes | Kill the process during a cache write | On next launch, the cache file is either the old valid version or the new valid version — never partial or corrupt |
| tree-cache-005 | flattened-cache-array | Load a cache with 100 entries and verify parent-child wiring | All entries with `parentPath` matching another entry's `path` are wired as children |
| tree-cache-006 | json-cache-format | Save a tree containing a file and a directory | The file on disk is valid JSON whose entries have all `FileTreeCacheEntry` fields |
| tree-cache-007 | cache-save-nonblocking | Make the cache location read-only and request a save | The save fails with a warning; the caller is not blocked and does not crash |

## Edge Cases

- **Corrupt cache file**: The loader MUST handle malformed JSON gracefully (handle-missing-cache) — log a warning and proceed as if no cache exists.
- **Cache file missing or unreadable**: Same behavior as a corrupt cache — empty/loading state.
- **Concurrent cache writes**: If a save is requested while a previous save is still in progress, the implementation SHOULD coalesce or serialize writes to avoid conflicts.
- **Orphaned entries**: An entry whose `parentPath` matches no entry in the array SHOULD be dropped on load rather than attached to the wrong parent.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `cacheFileName` | string | `file-tree-cache.json` | Name of the cache file |
| `cacheDirectory` | path | (app support directory) | Directory holding the cache; workspace coordinators use `cache-{entryID}` |

## Logging

Subsystem: `{{bundle_id}}` | Category: `DirectorySync`

| Event | Level | Message |
|-------|-------|---------|
| Cache load started | debug | `DirectorySync: loading cache from "{{path}}"` |
| Cache load succeeded | debug | `DirectorySync: cache loaded, {{count}} entries` |
| Cache load failed | warning | `DirectorySync: cache load failed: {{error}}` |
| Cache not found | debug | `DirectorySync: no cache file found, starting fresh` |
| Cache save started | debug | `DirectorySync: saving cache ({{count}} entries)` |
| Cache save succeeded | debug | `DirectorySync: cache saved to "{{path}}"` |
| Cache save failed | warning | `DirectorySync: cache save failed: {{error}}` |

## Platform Notes

- **SwiftUI (macOS)**: For atomic cache writes, write to a `.tmp` file in the same directory then use `FileManager.moveItem(at:to:)`, which is atomic on APFS/HFS+. Load and save on a background `DispatchQueue`.
- **SwiftUI (iOS / visionOS)**: Cache loading and saving work identically via `FileManager`.
- **Compose / React/Web**: Not applicable — this ingredient targets Apple platforms and TypeScript services; a web or Android implementation would use the platform's atomic-rename primitive in the same way.

## Design Decisions

**Decision**: Store the cache as a flattened array rather than a nested tree.
**Rationale**: A flat array is simple to stream, tolerant of partial corruption per entry, and keeps the format independent of tree depth; parent-child wiring is cheap to rebuild from `parentPath`.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [caching-strategy](agenticdevelopercookbook://compliance/performance#caching-strategy) | partial | Performance |
| [data-integrity](agenticdevelopercookbook://compliance/reliability#data-integrity) | partial | Reliability |
| [main-thread-freedom](agenticdevelopercookbook://compliance/performance#main-thread-freedom) | partial | Performance |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Directory Sync / Watch Lifecycle recipe |

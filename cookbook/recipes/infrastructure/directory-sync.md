---
id: 63659e2c-215a-44ed-b330-2bca8d88bd9a
title: "Directory Sync / Watch Lifecycle"
domain: agenticdevelopercookbook://recipes/infrastructure/directory-sync
type: recipe
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-03-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Lifecycle pattern for syncing an in-memory file tree with the filesystem via cache, full sync, watch, and surgical update"
platforms:
  - ios
  - macos
  - swift
  - typescript
tags:
  - directory-sync
  - infrastructure
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# Directory Sync / Watch Lifecycle

## Overview

A lifecycle pattern for synchronizing an in-memory file tree with the filesystem. The coordinator drives four sequential phases: cache load (instant display) followed by full sync (accurate rebuild) followed by watch (live updates) followed by surgical update (efficient patching). This ensures the UI displays a file tree immediately on launch while converging to an accurate, live-updated representation as quickly as possible.

## Terminology

| Term | Definition |
|------|-----------|
| Coordinator | The orchestrator (`DirectoryWatchCoordinator`) that owns the lifecycle and drives all four phases |
| File tree node | An in-memory representation of a single file or directory: path, name, metadata, and children |
| Cache | A JSON file (`file-tree-cache.json`) containing a flattened array of `FileTreeCacheEntry` values |
| Full sync | A complete traversal of the directory subtree that rebuilds the in-memory tree from scratch |
| Surgical update | A targeted reload that only rescans the directories affected by a filesystem change event |
| FSEvents | The macOS kernel subsystem that delivers file-level change notifications |
| Package | A directory that the OS treats as a single opaque file (e.g., `.app`, `.playground`, `.catnip-proj`) |
| Workspace | A collection of directory entries, each managed by its own coordinator via `WorkspaceDirectoryManager` |

## Behavioral Requirements

### Phase 1 — Cache Load

- **load-cached-tree**: On startup, the coordinator MUST attempt to load a cached tree from the JSON file `file-tree-cache.json` for instant display.
- **background-cache-load**: The cache MUST be loaded synchronously on a background queue so the main thread is never blocked.
- **handle-missing-cache**: If no cache file exists or the file cannot be read, the coordinator MUST present an empty or loading state. It MUST NOT crash or block.
- **publish-before-sync**: The loaded cache MUST be published to the UI before Phase 2 begins, so users see an instant tree.

### Phase 2 — Full Sync

- **rebuild-from-filesystem**: The coordinator MUST rebuild the entire file tree from the filesystem on a background queue.
- **parallel-top-level-scan**: Top-level directories MUST be scanned in parallel via an `OperationQueue`.
- **configurable-scan-workers**: Parallel scan concurrency MUST be controlled by a configurable `maxScanWorkers` property. The default value MUST be `3`. Valid range MUST be `1` to `8` inclusive. Values outside this range MUST be clamped.
- **file-tree-node-fields**: Each file tree node MUST contain the following fields:
  - `path` — absolute filesystem path (`String`)
  - `name` — display name (`String`)
  - `isDirectory` — whether the node is a directory (`Bool`)
  - `isPackage` — whether the node is a package directory (`Bool`)
  - `fileSize` — size in bytes (`Int?`, nil for directories)
  - `modificationDate` — last modification timestamp (`Date?`)
  - `children` — ordered child nodes (`[FileTreeNode]?`, nil for files)
- **save-cache-after-sync**: After the full sync completes, the coordinator MUST save the updated cache to disk as a fire-and-forget operation on a background queue. A save failure MUST NOT block or crash the coordinator.
- **publish-syncing-state**: The coordinator MUST publish an `isSyncing` boolean state that is `true` during Phase 2 and `false` after it completes. The UI SHOULD use this to display a status bar indicator.

### Phase 3 — Watch

- **start-fsevents-watch**: After full sync completes, the coordinator MUST start filesystem monitoring using FSEvents (macOS) with file-level granularity.
- **debounce-latency**: The FSEvents stream MUST use a debounce latency of `0.5` seconds to coalesce rapid changes.
- **exclude-path-prefixes**: The coordinator MUST exclude paths matching configurable prefixes from change processing. The default excluded prefixes MUST include `.git` and package directories.
- **dispatch-to-main-thread**: Change events from the FSEvents callback MUST be dispatched to the main thread for UI updates.

### Phase 4 — Surgical Update

- **surgical-reload-affected**: On receiving filesystem change events, the coordinator MUST only reload the children of the affected directories — not rebuild the full tree.
- **build-path-index**: The coordinator MUST build a path index from the changed file paths to identify the set of affected parent directories.
- **background-load-children**: New children for affected directories MUST be loaded on a background queue.
- **apply-on-main-thread**: The updated children MUST be applied to the in-memory tree on the main thread.
- **save-cache-after-update**: After a surgical update, the coordinator MUST save the updated cache to disk (fire-and-forget on a background queue).

### Cache Format

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

### FSEvents Configuration (macOS)

- **file-level-granularity**: The FSEvents stream MUST be created with `kFSEventStreamCreateFlagFileEvents` for file-level granularity.
- **utility-qos-queue**: The FSEvents dispatch queue MUST use utility QoS.
- **configurable-exclusions**: Excluded path prefixes MUST be configurable.
- **filter-excluded-paths**: The FSEvents callback MUST filter changed paths against the excluded prefixes before dispatching.

### Workspace Variant

- **coordinator-per-entry**: `WorkspaceDirectoryManager` MUST manage a pool of coordinators, one per workspace directory entry.
- **aggregate-syncing-state**: `WorkspaceDirectoryManager` MUST aggregate the `isSyncing` state across all coordinators. The workspace-level `isSyncing` MUST be `true` if any coordinator is syncing.
- **auto-discover-packages**: `WorkspaceDirectoryManager` MUST additionally scan for `.catnip-proj` packages for auto-discovery of projects.
- **dedicated-cache-directory**: Each coordinator in the workspace MUST use a dedicated cache directory named `cache-{entryID}`.

## States

| State | Behavior |
|-------|----------|
| No cache, first launch | Coordinator loads empty state, begins full sync immediately |
| Cache available | Coordinator displays cached tree instantly, then begins full sync in background |
| Full sync in progress | `isSyncing` is `true`, UI shows sync indicator |
| Full sync complete | `isSyncing` is `false`, watch phase starts, cache saved |
| Watch active, no changes | Coordinator idle, FSEvents stream listening |
| Filesystem change detected | Surgical update runs on affected directories only |
| Surgical update in progress | Affected directory children reloaded, tree patched, cache saved |
| Watch stopped (e.g., directory deleted) | Coordinator publishes empty tree, stops FSEvents stream |

## Accessibility

Not applicable — directory sync is an infrastructure component with no direct user-facing UI. UI presentation of the synced directory tree is handled by the file-tree-browser recipe.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| dirsync-001 | load-cached-tree, publish-before-sync | Launch with valid `file-tree-cache.json` on disk | Cached tree is published to UI before full sync begins |
| dirsync-002 | handle-missing-cache | Launch with no cache file on disk | Empty/loading state shown, full sync begins without error |
| dirsync-003 | handle-missing-cache | Launch with corrupt (invalid JSON) cache file | Empty/loading state shown, full sync begins without error |
| dirsync-004 | rebuild-from-filesystem, parallel-top-level-scan | Full sync on directory with 5 top-level subdirectories | All 5 subdirectories scanned, tree matches filesystem |
| dirsync-005 | configurable-scan-workers | Set `maxScanWorkers` to 0 | Value clamped to 1, scan proceeds with 1 worker |
| dirsync-006 | configurable-scan-workers | Set `maxScanWorkers` to 10 | Value clamped to 8, scan proceeds with 8 workers |
| dirsync-007 | file-tree-node-fields | Scan a directory containing a file (100 bytes, modified 2026-01-15) and a subdirectory | File node has correct `fileSize`, `modificationDate`, `isDirectory: false`; directory node has `isDirectory: true`, `children` populated |
| dirsync-008 | save-cache-after-sync | Full sync completes | `file-tree-cache.json` exists on disk with valid JSON content |
| dirsync-009 | publish-syncing-state | Observe `isSyncing` during full sync | Value is `true` during scan, `false` after completion |
| dirsync-010 | debounce-latency | Create 10 files within 0.3 seconds | Single coalesced change event delivered after 0.5s debounce |
| dirsync-011 | exclude-path-prefixes | Create a file inside `.git/` | No surgical update triggered, tree unchanged |
| dirsync-012 | surgical-reload-affected, build-path-index | Create a new file in subdirectory `src/` | Only `src/` children are reloaded; sibling directories untouched |
| dirsync-013 | apply-on-main-thread | Surgical update completes | Updated nodes visible in UI on main thread |
| dirsync-014 | save-cache-after-update | Surgical update completes | Cache file on disk reflects the new file |
| dirsync-015 | atomic-cache-writes | Kill process during cache write | On next launch, cache file is either the old valid version or the new valid version — never partial/corrupt |
| dirsync-016 | coordinator-per-entry | Workspace with 3 directory entries | 3 coordinators created, one per entry |
| dirsync-017 | aggregate-syncing-state | 1 of 3 workspace coordinators is syncing | Workspace-level `isSyncing` is `true` |
| dirsync-018 | aggregate-syncing-state | All 3 workspace coordinators finish syncing | Workspace-level `isSyncing` is `false` |
| dirsync-019 | auto-discover-packages | Workspace directory contains a `.catnip-proj` package | Package is auto-discovered and reported |
| dirsync-020 | dedicated-cache-directory | Two workspace entries with IDs "abc" and "def" | Cache directories are `cache-abc` and `cache-def` respectively |
| dirsync-021 | flattened-cache-array | Load cache with 100 entries, verify parent-child wiring | All entries with `parentPath` matching another entry's `path` are wired as children |

## Edge Cases

- **Large repository (100k+ files)**: Full sync SHOULD complete within a reasonable time. Parallel scanning (parallel-top-level-scan) and configurable concurrency (configurable-scan-workers) mitigate this. The UI MUST remain responsive during sync — all scanning is off the main thread.
- **Rapid filesystem changes**: The 0.5s debounce (debounce-latency) coalesces rapid changes into a single surgical update. If changes arrive faster than the update cycle, the coordinator SHOULD batch them rather than queueing unbounded updates.
- **Corrupt cache file**: The coordinator MUST handle malformed JSON gracefully (handle-missing-cache) — log a warning and proceed with full sync as if no cache exists.
- **Cache file missing or unreadable**: Same behavior as corrupt cache — empty/loading state, then full sync.
- **Network/remote drives**: FSEvents may not work reliably on network-mounted volumes. The coordinator SHOULD fall back to periodic polling or disable watch mode for non-local filesystems. Implementors SHOULD detect volume type and adapt.
- **Directory deleted while watching**: The coordinator MUST handle the root directory being deleted or unmounted. It SHOULD publish an empty tree and stop the FSEvents stream.
- **Permission denied on subdirectory**: The coordinator MUST skip inaccessible directories during scan and log a warning. It MUST NOT crash or abort the entire sync.
- **Symlink cycles**: The coordinator MUST NOT follow symlinks recursively into cycles. It SHOULD detect symlinks and either skip or represent them as leaf nodes.
- **Package directories**: Directories identified as packages (file-tree-node-fields `isPackage`) SHOULD NOT have their children scanned by default. They are treated as opaque files.
- **Concurrent cache writes**: If a surgical update triggers a cache save while a previous save is still in progress, the coordinator SHOULD coalesce or serialize writes to avoid conflicts.
- **Empty directory**: A directory with no children MUST be represented as a node with an empty `children` array, not `nil`.

## Logging

Subsystem: `{{bundle_id}}` | Category: `DirectorySync`

| Event | Level | Message |
|-------|-------|---------|
| Cache load started | debug | `DirectorySync: loading cache from "{{path}}"` |
| Cache load succeeded | debug | `DirectorySync: cache loaded, {{count}} entries` |
| Cache load failed | warning | `DirectorySync: cache load failed: {{error}}` |
| Cache not found | debug | `DirectorySync: no cache file found, starting fresh` |
| Full sync started | info | `DirectorySync: full sync started for "{{rootPath}}"` |
| Full sync completed | info | `DirectorySync: full sync completed, {{nodeCount}} nodes in {{duration}}s` |
| Cache save started | debug | `DirectorySync: saving cache ({{count}} entries)` |
| Cache save succeeded | debug | `DirectorySync: cache saved to "{{path}}"` |
| Cache save failed | warning | `DirectorySync: cache save failed: {{error}}` |
| Watch started | info | `DirectorySync: FSEvents watch started for "{{rootPath}}"` |
| Watch stopped | info | `DirectorySync: FSEvents watch stopped` |
| Change event received | debug | `DirectorySync: {{changeCount}} changes received, {{affectedDirCount}} directories affected` |
| Surgical update started | debug | `DirectorySync: surgical update for {{dirCount}} directories` |
| Surgical update completed | debug | `DirectorySync: surgical update completed in {{duration}}s` |
| Directory skipped (permission) | warning | `DirectorySync: skipped "{{path}}" — permission denied` |
| Excluded path filtered | debug | `DirectorySync: filtered {{count}} excluded paths` |
| Workspace coordinator created | debug | `DirectorySync: workspace coordinator created for entry "{{entryID}}"` |
| Workspace syncing state changed | debug | `DirectorySync: workspace isSyncing={{value}}` |
| Project auto-discovered | info | `DirectorySync: discovered .catnip-proj at "{{path}}"` |
| Scan worker count | debug | `DirectorySync: maxScanWorkers={{count}}` |

## Platform Notes

- **SwiftUI (macOS)**: Use `FSEventStreamCreate` with `kFSEventStreamCreateFlagFileEvents` and `kFSEventStreamCreateFlagUseCFTypes`. Schedule on a `DispatchQueue` with `.utility` QoS. Use `FileManager` for directory enumeration. Publish `isSyncing` via `@Published` on an `@Observable` or `ObservableObject` coordinator. For atomic cache writes, write to a `.tmp` file in the same directory then use `FileManager.moveItem(at:to:)` which is atomic on APFS/HFS+. Use `OperationQueue` with `maxConcurrentOperationCount` for parallel scanning.
- **SwiftUI (iOS / visionOS)**: FSEvents is not available on iOS or visionOS. Use `DispatchSource.makeFileSystemObjectSource` for directory-level monitoring on individual directories, or poll on a timer. File-level granularity is limited — surgical updates may need to rescan entire directories. Consider using `NSFilePresenter` / `NSFileCoordinator` for coordinated file access. On visionOS, the same iOS limitations apply. Cache loading and saving work identically via `FileManager`.

## Design Decisions

_None yet — decisions made during implementation should be recorded here._

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

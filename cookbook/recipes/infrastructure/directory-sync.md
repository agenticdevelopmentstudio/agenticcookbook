---
id: 63659e2c-215a-44ed-b330-2bca8d88bd9a
title: "Directory Sync / Watch Lifecycle"
domain: agenticdevelopercookbook://recipes/infrastructure/directory-sync
type: recipe
version: 2.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
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
ingredients:
  - agenticdevelopercookbook://ingredients/infrastructure/directory-tree-cache
  - agenticdevelopercookbook://ingredients/infrastructure/directory-tree-scanner
  - agenticdevelopercookbook://ingredients/infrastructure/filesystem-watcher
  - agenticdevelopercookbook://ingredients/infrastructure/directory-watch-coordinator
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Directory Sync / Watch Lifecycle

## Overview

A lifecycle pattern for synchronizing an in-memory file tree with the filesystem. The coordinator drives four sequential phases: cache load (instant display) followed by full sync (accurate rebuild) followed by watch (live updates) followed by surgical update (efficient patching). This ensures the UI displays a file tree immediately on launch while converging to an accurate, live-updated representation as quickly as possible.

The recipe composes four ingredients. The directory tree cache owns Phase 1 and the cache format. The directory tree scanner owns Phase 2 and the surgical reload of Phase 4. The filesystem watcher owns Phase 3. The directory watch coordinator owns the lifecycle, published state, and the workspace variant.

### Terminology

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

### Logging

Logging is specified per ingredient. The full event set under subsystem `{{bundle_id}}` and category `DirectorySync` is distributed as follows: cache load, cache save, and cache not found events are in the directory tree cache ingredient; full sync, surgical update, permission-skipped, and scan worker events are in the directory tree scanner ingredient; watch started, watch stopped, change received, and excluded-path events are in the filesystem watcher ingredient; the workspace coordinator, workspace syncing state, and project auto-discovery events are in the directory watch coordinator ingredient.

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Directory tree cache | `agenticdevelopercookbook://ingredients/infrastructure/directory-tree-cache` | Phase 1: loads the JSON cache for instant display and writes it atomically after every change | Yes | Cache directory (a dedicated `cache-{entryID}` directory per workspace entry) |
| Directory tree scanner | `agenticdevelopercookbook://ingredients/infrastructure/directory-tree-scanner` | Phase 2 and Phase 4: full rebuild and surgical reload of affected directories | Yes | `maxScanWorkers` (default 3, clamped to 1-8) |
| Filesystem watcher | `agenticdevelopercookbook://ingredients/infrastructure/filesystem-watcher` | Phase 3: file-level change notifications, debounced and filtered | Yes | Debounce latency (0.5 seconds), excluded path prefixes (default `.git` and package directories) |
| Directory watch coordinator | `agenticdevelopercookbook://ingredients/infrastructure/directory-watch-coordinator` | Owns the lifecycle, publishes the tree and `isSyncing`, applies updates on the main thread; the workspace manager pools one per entry | Yes | Entry ID for workspace use |

## Integration Requirements

- **phase-ordering**: The coordinator MUST run the phases in this order: cache load, full sync, watch, surgical update. Watch MUST NOT start before the full sync completes, and a surgical update MUST NOT run before the watch has delivered a change.
- **cache-feeds-first-publish**: The tree produced by the directory tree cache MUST be handed to the coordinator and published before the scanner begins its full sync, so a valid cache always displays before the scan finishes.
- **sync-result-replaces-cache-tree**: When the scanner completes its full sync, the coordinator MUST replace the published tree with the scanned tree and then trigger a cache save of that tree.
- **watch-events-drive-surgical-update**: The changed paths the filesystem watcher delivers (after debounce and exclusion filtering) MUST be passed to the scanner's path index so only the affected directories are reloaded, and the coordinator MUST then apply the result and trigger a cache save.
- **shared-exclusion-policy**: The watcher's excluded prefixes and the scanner's treatment of package directories MUST agree: a path the watcher excludes MUST NOT cause a surgical update, and a package directory the scanner treats as opaque MUST NOT have its children reported as changed nodes.
- **failure-isolation**: A cache load failure, a cache save failure, or a permission-denied directory MUST NOT prevent the remaining phases from running; the coordinator MUST continue from the next phase.
- **main-thread-boundary**: Cache load, scanning, and cache saves MUST run off the main thread; only the application of updated nodes to the published tree and the `isSyncing` publication MUST occur on the main thread.

## Layout

The four phases are a pipeline around one owner. This is a non-UI recipe, so the layout is the logical arrangement of the components and the order of the data flow.

```
 launch
   │
   ▼
 ┌──────────────────────┐   cached tree   ┌──────────────────────────┐
 │ Directory tree cache │ ───────────────▶│                          │──▶ published tree (UI)
 └──────────────────────┘                  │ Directory watch          │──▶ isSyncing (UI)
 ┌──────────────────────┐   scanned tree  │ coordinator              │
 │ Directory tree       │ ───────────────▶│  (one per directory;     │
 │ scanner              │ ◀───────────────│   workspace manager      │
 └──────────────────────┘  changed paths  │   pools one per entry)   │
 ┌──────────────────────┐ ───────────────▶│                          │
 │ Filesystem watcher   │                 └─────────────┬────────────┘
 └──────────────────────┘                               │ save after sync / update
                                                        ▼
                                              Directory tree cache (atomic write)
```

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| In-memory file tree | Directory tree scanner (full sync, surgical reload) and directory tree cache (initial load) | Coordinator, then the UI | one-way | The coordinator publishes the tree; updates are applied on the main thread |
| `isSyncing` | Coordinator | UI status bar, workspace manager | one-way | Published boolean; `true` only during the full sync; the workspace manager aggregates it with logical OR |
| Cache file (`file-tree-cache.json`) | Coordinator after sync or update | Directory tree cache on the next launch | one-way | Atomic write to a temporary file followed by a rename |
| Changed paths | Filesystem watcher | Scanner path index via the coordinator | one-way | Debounced, exclusion-filtered batch delivered on the main thread |
| Excluded path prefixes | Configuration | Filesystem watcher | one-way | Configurable list, default `.git` and package directories |
| Scan concurrency | Configuration | Scanner | one-way | `maxScanWorkers`, default 3, clamped to 1-8 |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| dirsync-001 | load-cached-tree, publish-before-sync, cache-feeds-first-publish | Launch with valid `file-tree-cache.json` on disk | Cached tree is published to UI before full sync begins |
| dirsync-002 | handle-missing-cache, failure-isolation | Launch with no cache file on disk | Empty/loading state shown, full sync begins without error |
| dirsync-003 | handle-missing-cache, failure-isolation | Launch with corrupt (invalid JSON) cache file | Empty/loading state shown, full sync begins without error |
| dirsync-008 | save-cache-after-sync, sync-result-replaces-cache-tree | Full sync completes | `file-tree-cache.json` exists on disk with valid JSON content |
| dirsync-009 | publish-syncing-state | Observe `isSyncing` during full sync | Value is `true` during scan, `false` after completion |
| dirsync-011 | exclude-path-prefixes, shared-exclusion-policy | Create a file inside `.git/` | No surgical update triggered, tree unchanged |
| dirsync-012 | surgical-reload-affected, build-path-index, watch-events-drive-surgical-update | Create a new file in subdirectory `src/` | Only `src/` children are reloaded; sibling directories untouched |
| dirsync-013 | apply-on-main-thread, main-thread-boundary | Surgical update completes | Updated nodes visible in UI on main thread |
| dirsync-014 | save-cache-after-update | Surgical update completes | Cache file on disk reflects the new file |
| dirsync-022 | phase-ordering | Launch and observe the phase sequence | Cache load, then full sync, then watch start; no watch event is processed before the full sync completes |
| dirsync-023 | failure-isolation | Scan a tree where one subdirectory is permission-denied | That directory is skipped with a warning; the remaining directories are scanned and the watch phase still starts |

Vectors dirsync-004 to dirsync-007, dirsync-010, dirsync-015 to dirsync-021 are single-ingredient vectors and appear in the ingredients under their new IDs: scanner vectors (dirsync-004, -005, -006, -007) in the directory tree scanner; watcher vector (dirsync-010) in the filesystem watcher; cache vectors (dirsync-015, -021) in the directory tree cache; and workspace vectors (dirsync-016 to dirsync-020) in the directory watch coordinator.

## Edge Cases

- **Large repository (100k+ files)**: Full sync SHOULD complete within a reasonable time. Parallel scanning and configurable concurrency mitigate this. The UI MUST remain responsive during sync — all scanning is off the main thread (main-thread-boundary).
- **Rapid filesystem changes**: The debounce coalesces rapid changes into a single surgical update. If changes arrive faster than the update cycle, the coordinator SHOULD batch them rather than queueing unbounded updates.
- **Corrupt or missing cache file**: Handled as in the directory tree cache ingredient: log a warning and proceed with full sync as if no cache exists (failure-isolation).
- **Network/remote drives**: FSEvents may not work reliably on network-mounted volumes. The coordinator SHOULD fall back to periodic polling or disable watch mode for non-local filesystems. Implementors SHOULD detect volume type and adapt.
- **Directory deleted while watching**: The coordinator MUST handle the root directory being deleted or unmounted. It SHOULD publish an empty tree and stop the FSEvents stream.
- **Permission denied on subdirectory**: The coordinator MUST skip inaccessible directories during scan and log a warning. It MUST NOT crash or abort the entire sync.
- **Symlink cycles**: The coordinator MUST NOT follow symlinks recursively into cycles. It SHOULD detect symlinks and either skip or represent them as leaf nodes.
- **Package directories**: Directories identified as packages (`isPackage`) SHOULD NOT have their children scanned by default. They are treated as opaque files (shared-exclusion-policy).
- **Concurrent cache writes**: If a surgical update triggers a cache save while a previous save is still in progress, the coordinator SHOULD coalesce or serialize writes to avoid conflicts.
- **Empty directory**: A directory with no children MUST be represented as a node with an empty `children` array, not `nil`.

## Platform Notes

- **SwiftUI (macOS)**: Use `FSEventStreamCreate` with `kFSEventStreamCreateFlagFileEvents` and `kFSEventStreamCreateFlagUseCFTypes`. Schedule on a `DispatchQueue` with `.utility` QoS. Use `FileManager` for directory enumeration. Publish `isSyncing` via `@Published` on an `@Observable` or `ObservableObject` coordinator. For atomic cache writes, write to a `.tmp` file in the same directory then use `FileManager.moveItem(at:to:)` which is atomic on APFS/HFS+. Use `OperationQueue` with `maxConcurrentOperationCount` for parallel scanning.
- **SwiftUI (iOS / visionOS)**: FSEvents is not available on iOS or visionOS. Use `DispatchSource.makeFileSystemObjectSource` for directory-level monitoring on individual directories, or poll on a timer. File-level granularity is limited — surgical updates may need to rescan entire directories. Consider using `NSFilePresenter` / `NSFileCoordinator` for coordinated file access. On visionOS, the same iOS limitations apply. Cache loading and saving work identically via `FileManager`.
- **Compose**: Not applicable as written — FSEvents and `FileManager` are Apple frameworks. An Android implementation would use `FileObserver` for watching and expose `isSyncing` and the tree as `StateFlow` values; the integration requirements apply unchanged.
- **React/Web**: Not applicable to browser runtimes, which have no general filesystem watching. A Node.js (TypeScript) implementation would use a native watcher such as `fs.watch` or chokidar behind the same requirements.

## Design Decisions

**Decision**: Split the lifecycle into a cache, a scanner, a watcher, and a thin coordinator instead of one monolithic coordinator.
**Rationale**: Each component has independent requirements and can be reused or replaced without touching the others; the coordinator owns only ordering, published state, and main-thread application. This replaces the earlier note that no design decisions had been recorded yet.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [main-thread-freedom](agenticdevelopercookbook://compliance/performance#main-thread-freedom) | partial | Performance |
| [graceful-degradation](agenticdevelopercookbook://compliance/reliability#graceful-degradation) | partial | Reliability |
| [data-integrity](agenticdevelopercookbook://compliance/reliability#data-integrity) | partial | Reliability |

> Status is `partial`: this recipe specifies the integration-level requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-10-04 | Mike Fullerton | Restructure into recipe shape; extract component behavior into ingredients |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

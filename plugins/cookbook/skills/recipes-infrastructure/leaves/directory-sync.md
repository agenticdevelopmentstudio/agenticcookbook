<!-- leaf: recipes-infrastructure/directory-sync · source: recipes/infrastructure/directory-sync.md -->

**Rules** (cite as `recipes-infrastructure/directory-sync#<slug>`):

- `load-cached-tree` MUST
- `background-cache-load` MUST
- `handle-missing-cache` MUST
- `publish-before-sync` MUST
- `rebuild-from-filesystem` MUST
- `parallel-top-level-scan` MUST
- `configurable-scan-workers` MUST
- `file-tree-node-fields` MUST
- `save-cache-after-sync` MUST
- `publish-syncing-state` MUST
- `start-fsevents-watch` MUST
- `debounce-latency` MUST
- `exclude-path-prefixes` MUST
- `dispatch-to-main-thread` MUST
- `surgical-reload-affected` MUST
- `build-path-index` MUST
- `background-load-children` MUST
- `apply-on-main-thread` MUST
- `save-cache-after-update` MUST
- `json-cache-format` MUST
- `flattened-cache-array` MUST
- `atomic-cache-writes` MUST
- `file-level-granularity` MUST
- `utility-qos-queue` MUST
- `configurable-exclusions` MUST
- `filter-excluded-paths` MUST
- `coordinator-per-entry` MUST
- `aggregate-syncing-state` MUST
- `auto-discover-packages` MUST
- `dedicated-cache-directory` MUST

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

## Platform Notes

- **SwiftUI (macOS)**: Use `FSEventStreamCreate` with `kFSEventStreamCreateFlagFileEvents` and `kFSEventStreamCreateFlagUseCFTypes`. Schedule on a `DispatchQueue` with `.utility` QoS. Use `FileManager` for directory enumeration. Publish `isSyncing` via `@Published` on an `@Observable` or `ObservableObject` coordinator. For atomic cache writes, write to a `.tmp` file in the same directory then use `FileManager.moveItem(at:to:)` which is atomic on APFS/HFS+. Use `OperationQueue` with `maxConcurrentOperationCount` for parallel scanning.
- **SwiftUI (iOS / visionOS)**: FSEvents is not available on iOS or visionOS. Use `DispatchSource.makeFileSystemObjectSource` for directory-level monitoring on individual directories, or poll on a timer. File-level granularity is limited — surgical updates may need to rescan entire directories. Consider using `NSFilePresenter` / `NSFileCoordinator` for coordinated file access. On visionOS, the same iOS limitations apply. Cache loading and saving work identically via `FileManager`.

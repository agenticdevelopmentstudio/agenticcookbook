
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


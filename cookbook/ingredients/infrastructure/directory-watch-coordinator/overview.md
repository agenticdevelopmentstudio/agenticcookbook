
The directory watch coordinator (`DirectoryWatchCoordinator`) owns the sync lifecycle for a single directory: it publishes the in-memory tree and an `isSyncing` state, saves the cache after every change to the tree, and applies updates to the tree on the main thread. The workspace manager (`WorkspaceDirectoryManager`) pools one coordinator per workspace directory entry and aggregates their syncing state. The coordinator does not scan, cache, or watch by itself — it drives the cache, scanner, and watcher ingredients (see the Directory Sync recipe for the phase wiring).

### Terminology

| Term | Definition |
|------|-----------|
| Coordinator | The orchestrator (`DirectoryWatchCoordinator`) that owns the lifecycle for one directory |
| Workspace | A collection of directory entries, each managed by its own coordinator via `WorkspaceDirectoryManager` |
| Package | A directory that the OS treats as a single opaque file (e.g., `.app`, `.playground`, `.catnip-proj`) |


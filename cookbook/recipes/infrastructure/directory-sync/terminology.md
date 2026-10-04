
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


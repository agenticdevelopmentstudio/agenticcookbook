
| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| In-memory file tree | Directory tree scanner (full sync, surgical reload) and directory tree cache (initial load) | Coordinator, then the UI | one-way | The coordinator publishes the tree; updates are applied on the main thread |
| `isSyncing` | Coordinator | UI status bar, workspace manager | one-way | Published boolean; `true` only during the full sync; the workspace manager aggregates it with logical OR |
| Cache file (`file-tree-cache.json`) | Coordinator after sync or update | Directory tree cache on the next launch | one-way | Atomic write to a temporary file followed by a rename |
| Changed paths | Filesystem watcher | Scanner path index via the coordinator | one-way | Debounced, exclusion-filtered batch delivered on the main thread |
| Excluded path prefixes | Configuration | Filesystem watcher | one-way | Configurable list, default `.git` and package directories |
| Scan concurrency | Configuration | Scanner | one-way | `maxScanWorkers`, default 3, clamped to 1-8 |


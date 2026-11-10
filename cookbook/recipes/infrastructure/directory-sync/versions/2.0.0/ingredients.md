
| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Directory tree cache | `agenticdevelopercookbook://ingredients/infrastructure/directory-tree-cache` | Phase 1: loads the JSON cache for instant display and writes it atomically after every change | Yes | Cache directory (a dedicated `cache-{entryID}` directory per workspace entry) |
| Directory tree scanner | `agenticdevelopercookbook://ingredients/infrastructure/directory-tree-scanner` | Phase 2 and Phase 4: full rebuild and surgical reload of affected directories | Yes | `maxScanWorkers` (default 3, clamped to 1-8) |
| Filesystem watcher | `agenticdevelopercookbook://ingredients/infrastructure/filesystem-watcher` | Phase 3: file-level change notifications, debounced and filtered | Yes | Debounce latency (0.5 seconds), excluded path prefixes (default `.git` and package directories) |
| Directory watch coordinator | `agenticdevelopercookbook://ingredients/infrastructure/directory-watch-coordinator` | Owns the lifecycle, publishes the tree and `isSyncing`, applies updates on the main thread; the workspace manager pools one per entry | Yes | Entry ID for workspace use |


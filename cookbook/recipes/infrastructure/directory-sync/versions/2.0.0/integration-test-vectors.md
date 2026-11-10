
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


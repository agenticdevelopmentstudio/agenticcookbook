
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


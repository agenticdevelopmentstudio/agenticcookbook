
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| ws-018 | workspace-package-format, sqlite-table-schema | Inspect workspace package on disk | `.catnip-workspace` directory contains `workspace.db` with tables: workspace, entries, discovered_projects, settings |
| ws-019 | sync-on-entry-change | Add a directory entry via UI | Entry appears in `entries` table, `syncEntries` fires, new coordinator created |
| ws-020 | sync-on-entry-change | Remove a directory entry via context menu | Entry removed from `entries` table, coordinator stopped and removed |
| ws-021 | coordinator-pool-manager | Workspace with 3 directory entries | WorkspaceDirectoryManager has 3 coordinators |
| ws-022 | aggregate-sync-state | 1 of 3 coordinators syncing | Workspace-level `isSyncing` is `true` |
| ws-023 | aggregate-sync-state | All 3 coordinators idle | Workspace-level `isSyncing` is `false` |
| ws-024 | auto-discover-projects | Directory entry contains a new `.catnip-proj` package | `onDiscoveryChanged` fires, `discovered_projects` table updated |
| ws-025 | per-entry-cache-dir | Workspace with entry ID "abc" | Cache directory is `cache-abc` within workspace package |
| ws-026 | auto-correct-entry-type | Entry has type `.project` but path is `/Users/me/Code` (no `.catnip-proj` suffix) | Type auto-corrected to `.directory` |
| ws-027 | prevent-self-referential | Attempt to add workspace's own `.catnip-workspace` path as an entry | Add rejected, warning logged |
| ws-028 | prevent-duplicate-entry | Attempt to add `/Users/me/Code` when it already exists as an entry | Add rejected |


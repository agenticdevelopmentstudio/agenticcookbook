
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| dir-coordinator-001 | publish-syncing-state | Observe `isSyncing` during full sync | Value is `true` during the scan, `false` after completion |
| dir-coordinator-002 | save-cache-after-sync | Full sync completes | `file-tree-cache.json` exists on disk with valid JSON content |
| dir-coordinator-003 | apply-on-main-thread | Surgical update completes | Updated nodes are applied to the tree on the main thread |
| dir-coordinator-004 | save-cache-after-update | Surgical update completes | Cache file on disk reflects the new file |
| dir-coordinator-005 | coordinator-per-entry | Workspace with 3 directory entries | 3 coordinators are created, one per entry |
| dir-coordinator-006 | aggregate-syncing-state | 1 of 3 workspace coordinators is syncing | Workspace-level `isSyncing` is `true` |
| dir-coordinator-007 | aggregate-syncing-state | All 3 workspace coordinators finish syncing | Workspace-level `isSyncing` is `false` |
| dir-coordinator-008 | auto-discover-packages | Workspace directory contains a `.catnip-proj` package | Package is auto-discovered and reported |
| dir-coordinator-009 | dedicated-cache-directory | Two workspace entries with IDs "abc" and "def" | Cache directories are `cache-abc` and `cache-def` respectively |
| dir-coordinator-010 | publish-before-sync | Launch with a valid cache on disk | The cached tree is published before the full sync starts |


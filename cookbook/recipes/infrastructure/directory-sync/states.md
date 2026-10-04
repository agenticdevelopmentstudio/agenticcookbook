
| State | Behavior |
|-------|----------|
| No cache, first launch | Coordinator loads empty state, begins full sync immediately |
| Cache available | Coordinator displays cached tree instantly, then begins full sync in background |
| Full sync in progress | `isSyncing` is `true`, UI shows sync indicator |
| Full sync complete | `isSyncing` is `false`, watch phase starts, cache saved |
| Watch active, no changes | Coordinator idle, FSEvents stream listening |
| Filesystem change detected | Surgical update runs on affected directories only |
| Surgical update in progress | Affected directory children reloaded, tree patched, cache saved |
| Watch stopped (e.g., directory deleted) | Coordinator publishes empty tree, stops FSEvents stream |


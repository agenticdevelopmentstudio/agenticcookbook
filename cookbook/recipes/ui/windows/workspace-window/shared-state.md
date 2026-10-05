
| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Entries and discovered projects | Workspace Document | Workspace Browser sidebar | one-way | Observable document model |
| Aggregated `isSyncing` | Workspace Document (directory-watch pool) | Sync indicator in the browser | one-way | Any coordinator syncing sets it true |
| Add and remove commands | Workspace Browser | Workspace Document | one-way | Validated, then `syncEntries` reconciles the pool |
| Sidebar proportion | Window split divider | Workspace Document `settings` table | two-way | Persisted on change, restored on open |
| Window frame | Window | Window Frame Persistence | two-way | Autosave name from workspace path hash |



Subsystem: `{{bundle_id}}` | Category: `GitStatus`

| Event | Level | Message |
|-------|-------|---------|
| Refresh started | debug | `GitStatus: refresh started for "{{repoPath}}"` |
| Refresh completed | debug | `GitStatus: refresh completed, {{count}} files with status` |
| Refresh timed out | debug | `GitStatus: refresh timed out after {{timeout}}s` |
| Stale result discarded | debug | `GitStatus: discarded stale result (request {{id}})` |


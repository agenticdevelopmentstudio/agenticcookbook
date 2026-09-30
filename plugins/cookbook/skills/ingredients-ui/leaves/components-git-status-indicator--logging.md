<!-- leaf: ingredients-ui/components-git-status-indicator--logging · source: ingredients/ui/components/git-status-indicator.md -->

# Git Status Indicator

## Logging

Subsystem: `{{bundle_id}}` | Category: `GitStatus`

| Event | Level | Message |
|-------|-------|---------|
| Refresh started | debug | `GitStatus: refresh started for "{{repoPath}}"` |
| Refresh completed | debug | `GitStatus: refresh completed, {{count}} files with status` |
| Refresh timed out | debug | `GitStatus: refresh timed out after {{timeout}}s` |
| Stale result discarded | debug | `GitStatus: discarded stale result (request {{id}})` |

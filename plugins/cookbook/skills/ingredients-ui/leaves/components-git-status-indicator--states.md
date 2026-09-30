<!-- leaf: ingredients-ui/components-git-status-indicator--states · source: ingredients/ui/components/git-status-indicator.md -->

# Git Status Indicator

## States

| State | Appearance |
|-------|-----------|
| No git status | Badge not shown |
| File has status | Single character badge with color |
| Directory has aggregated status | Highest-priority child status shown |
| Git command in progress | Previous status remains until new result arrives |
| Git command failed/timed out | Previous status cleared or retained with stale indicator |

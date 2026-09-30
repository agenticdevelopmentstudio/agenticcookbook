<!-- leaf: recipes-ui/windows-project-window--logging · source: recipes/ui/windows/project-window.md -->

# Project Window

## Logging

Subsystem: `{{bundle_id}}` | Category: `ProjectWindow`

| Event | Level | Message |
|-------|-------|---------|
| Window opened | info | `ProjectWindow: opened for "{{projectPath}}"` |
| Window closed | info | `ProjectWindow: closed for "{{projectPath}}"` |
| Load initial started | debug | `ProjectWindow: loadInitial started` |
| Load initial completed | debug | `ProjectWindow: loadInitial completed` |
| File watcher started | debug | `ProjectWindow: startWatching for "{{projectPath}}"` |
| File watcher stopped | debug | `ProjectWindow: stopWatching for "{{projectPath}}"` |
| File watcher failed | error | `ProjectWindow: startWatching failed: {{error}}` |
| Processes terminated | debug | `ProjectWindow: terminateAll called` |
| Sessions panel toggled | debug | `ProjectWindow: sessions panel toggled to {{visible\|hidden}}` |
| File tree toggled | debug | `ProjectWindow: file tree toggled to {{visible\|hidden}}` |
| Terminal toggled | debug | `ProjectWindow: terminal toggled to {{visible\|hidden}}` |
| Inspector toggled | debug | `ProjectWindow: inspector toggled to {{visible\|hidden}}` |
| Proportions saved | debug | `ProjectWindow: proportions saved (sessions={{s}}, fileTree={{f}}, detailSplit={{d}})` |
| Settings sheet presented | debug | `ProjectWindow: settings sheet presented` |
| Frame autosave set | debug | `ProjectWindow: frame autosave name "{{hash}}"` |
| Auto-open terminal | debug | `ProjectWindow: auto-opening terminal per user settings` |

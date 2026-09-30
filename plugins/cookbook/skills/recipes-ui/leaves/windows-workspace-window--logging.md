<!-- leaf: recipes-ui/windows-workspace-window--logging · source: recipes/ui/windows/workspace-window.md -->

# Workspace Window

## Logging

Subsystem: `{{bundle_id}}` | Category: `WorkspaceWindow`

| Event | Level | Message |
|-------|-------|---------|
| Window opened | debug | `WorkspaceWindow: opened "{{workspacePath}}"` |
| Window closed | debug | `WorkspaceWindow: closed "{{workspacePath}}"` |
| Frame autosave set | debug | `WorkspaceWindow: autosave name "{{hashedName}}"` |
| Sidebar proportion changed | debug | `WorkspaceWindow: sidebar proportion changed to {{value}}` |
| Entry added | info | `WorkspaceWindow: added {{entryType}} entry "{{path}}"` |
| Entry removed | info | `WorkspaceWindow: removed {{entryType}} entry "{{path}}"` |
| Entry selected | debug | `WorkspaceWindow: selected entry "{{name}}" ({{entryType}})` |
| Entry type migrated | warning | `WorkspaceWindow: migrated entry "{{path}}" from .project to .directory (path does not end with .catnip-proj)` |
| Project opened | info | `WorkspaceWindow: opening project "{{path}}"` |
| Project open failed | error | `WorkspaceWindow: failed to open project "{{path}}": {{error}}` |
| Self-referential add rejected | warning | `WorkspaceWindow: rejected self-referential add of "{{path}}"` |
| Duplicate add rejected | warning | `WorkspaceWindow: rejected duplicate entry "{{path}}"` |
| Discovery changed | debug | `WorkspaceWindow: discovery changed for entry "{{entryID}}", {{count}} projects found` |
| Sync entries triggered | debug | `WorkspaceWindow: syncEntries triggered, {{entryCount}} entries` |
| Coordinator created | debug | `WorkspaceWindow: coordinator created for entry "{{entryID}}"` |
| Coordinator removed | debug | `WorkspaceWindow: coordinator removed for entry "{{entryID}}"` |
| Workspace DB opened | debug | `WorkspaceWindow: database opened at "{{dbPath}}"` |
| Workspace DB error | error | `WorkspaceWindow: database error: {{error}}` |
| Workspace DB recreated | warning | `WorkspaceWindow: database recreated due to corruption` |
| Empty state displayed | debug | `WorkspaceWindow: showing welcome empty state` |
| Add directory picker shown | debug | `WorkspaceWindow: showing directory picker` |
| Add project picker shown | debug | `WorkspaceWindow: showing project picker` |
| Non-existent entry path | warning | `WorkspaceWindow: entry "{{path}}" does not exist on disk` |

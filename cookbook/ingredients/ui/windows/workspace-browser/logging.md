
Subsystem: `{{bundle_id}}` | Category: `WorkspaceWindow`

The window-level events are emitted by the Workspace Window recipe through this ingredient's category.

| Event | Level | Message |
|-------|-------|---------|
| Window opened | debug | `WorkspaceWindow: opened "{{workspacePath}}"` |
| Window closed | debug | `WorkspaceWindow: closed "{{workspacePath}}"` |
| Frame autosave set | debug | `WorkspaceWindow: autosave name "{{hashedName}}"` |
| Sidebar proportion changed | debug | `WorkspaceWindow: sidebar proportion changed to {{value}}` |
| Entry selected | debug | `WorkspaceWindow: selected entry "{{name}}" ({{entryType}})` |
| Project opened | info | `WorkspaceWindow: opening project "{{path}}"` |
| Project open failed | error | `WorkspaceWindow: failed to open project "{{path}}": {{error}}` |
| Empty state displayed | debug | `WorkspaceWindow: showing welcome empty state` |
| Add directory picker shown | debug | `WorkspaceWindow: showing directory picker` |
| Add project picker shown | debug | `WorkspaceWindow: showing project picker` |
| Non-existent entry path | warning | `WorkspaceWindow: entry "{{path}}" does not exist on disk` |


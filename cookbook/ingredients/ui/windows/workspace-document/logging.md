
Subsystem: `{{bundle_id}}` | Category: `WorkspaceWindow`

| Event | Level | Message |
|-------|-------|---------|
| Entry added | info | `WorkspaceWindow: added {{entryType}} entry "{{path}}"` |
| Entry removed | info | `WorkspaceWindow: removed {{entryType}} entry "{{path}}"` |
| Entry type migrated | warning | `WorkspaceWindow: migrated entry "{{path}}" from .project to .directory (path does not end with .catnip-proj)` |
| Self-referential add rejected | warning | `WorkspaceWindow: rejected self-referential add of "{{path}}"` |
| Duplicate add rejected | warning | `WorkspaceWindow: rejected duplicate entry "{{path}}"` |
| Discovery changed | debug | `WorkspaceWindow: discovery changed for entry "{{entryID}}", {{count}} projects found` |
| Sync entries triggered | debug | `WorkspaceWindow: syncEntries triggered, {{entryCount}} entries` |
| Coordinator created | debug | `WorkspaceWindow: coordinator created for entry "{{entryID}}"` |
| Coordinator removed | debug | `WorkspaceWindow: coordinator removed for entry "{{entryID}}"` |
| Workspace DB opened | debug | `WorkspaceWindow: database opened at "{{dbPath}}"` |
| Workspace DB error | error | `WorkspaceWindow: database error: {{error}}` |
| Workspace DB recreated | warning | `WorkspaceWindow: database recreated due to corruption` |


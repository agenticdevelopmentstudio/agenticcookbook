
| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Workspace Browser | `agenticdevelopercookbook://ingredients/ui/windows/workspace-browser` | Sidebar, detail pane, context menus, welcome state, sync indicator | Yes | Sidebar default 0.3 |
| Workspace Document | `agenticdevelopercookbook://ingredients/ui/windows/workspace-document` | Persisted entries, directory-watch pool, discovery, validation | Yes | Cache dir `cache-{entryID}` |
| Empty State | `agenticdevelopercookbook://ingredients/ui/components/empty-state` | Welcome view when no entry is selected | Yes | Actions: Add Directory, Add Project |
| Window Frame Persistence | `agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence` | Persists window position and size | Yes | Autosave name = hash of the workspace file path |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Window-level logging | Yes | Category `WorkspaceWindow` |


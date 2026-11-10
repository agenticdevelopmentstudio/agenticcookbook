
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Workspace Browser | [adc.ingredient.ui.windows.workspace-browser](cookbook:7264c7b6-593e-4ed9-8974-f5ea5e4db123) | Sidebar, detail pane, context menus, welcome state, sync indicator | Yes | Sidebar default 0.3 |
| Workspace Document | [adc.ingredient.ui.windows.workspace-document](cookbook:cf2b27b3-199e-4779-ac15-7923a9fefc1f) | Persisted entries, directory-watch pool, discovery, validation | Yes | Cache dir `cache-{entryID}` |
| Empty State | [adc.ingredient.ui.components.empty-state](cookbook:ce2af25c-4f18-41ae-91b9-342e363449b3) | Welcome view when no entry is selected | Yes | Actions: Add Directory, Add Project |
| Window Frame Persistence | [adc.ingredient.infrastructure.window-frame-persistence](cookbook:85d04a9b-5692-4025-a489-eac8bbb14663) | Persists window position and size | Yes | Autosave name = hash of the workspace file path |
| Logging | [adc.ingredient.infrastructure.logging](cookbook:7c2049c7-89d9-4135-b657-dbd03cdd19a0) | Window-level logging | Yes | Category `WorkspaceWindow` |


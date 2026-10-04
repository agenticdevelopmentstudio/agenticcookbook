
```
+-------------------------------------------------------+
| Workspace: MyWorkspace                                |
+------------------+------------------------------------+
|                  |                                    |
| PROJECTS         |                                    |
|  [pkg] App.catnip|    Entry Detail View               |
|  [pkg] Lib.catnip|    or                              |
|                  |    Empty State / Welcome            |
| DIRECTORIES      |    ┌─────────────────────┐         |
|  [dir] ~/Code    |    │ [icon]              │         |
|    [pkg] Found1  |    │ Welcome to Workspace│         |
|    [pkg] Found2  |    │                     │         |
|  [dir] ~/Plugins |    │ [Add Directory]     │         |
|    [pkg] Found3  |    │ [Add Project]       │         |
|                  |    └─────────────────────┘         |
|                  |                                    |
+--[SyncProgressBar]+------------------------------------+
```

- **Layout**: `HSplitView` — sidebar (left), detail pane (right)
- **Sidebar width**: Proportional, default 0.3 of window width, user-adjustable via split divider
- **Section headers**: "Projects" and "Directories", uppercase, secondary color, small font weight
- **Project row**: Package icon (`shippingbox.fill`, orange) + project name (primary text) + path (secondary text, truncated)
- **Directory row**: Folder icon (`folder.fill`, accent) + directory name
- **Discovered project row**: Package icon (`shippingbox.fill`, orange) + project name, indented within disclosure group
- **Sync indicator**: `SyncProgressBar` at the bottom of the sidebar, visible only when syncing
- **Detail pane background**: Standard window background
- **Empty state**: Centered per [empty-state.md](../../../ingredients/ui/components/empty-state.md) with folder icon, welcome heading, and action buttons


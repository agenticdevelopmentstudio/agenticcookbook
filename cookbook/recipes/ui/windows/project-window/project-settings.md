
Layout proportions and pane visibility are persisted per-project in ProjectSettings:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `sessionPanelProportion` | `Double` | `0.15` | Sessions panel width as fraction of window width |
| `fileTreeProportion` | `Double` | `0.20` | File tree panel width as fraction of window width |
| `detailSplitRatio` | `Double` | `0.5` | Vertical split ratio between editor and terminal (0.0 = all terminal, 1.0 = all editor) |
| `isSessionPanelVisible` | `Bool` | `true` | Whether the sessions panel is shown |
| `isFileViewerVisible` | `Bool` | `true` | Whether the file tree panel is shown |
| `isTerminalVisible` | `Bool` | `true` | Whether the terminal pane is shown |
| `isInspectorPresented` | `Bool` | `false` | Whether the inspector panel is shown |

- **persist-project-settings**: All settings in this table MUST be persisted per-project and restored on next open.
- **immediate-settings-save**: Changes to visibility or proportions MUST be written to ProjectSettings immediately (no manual save action).


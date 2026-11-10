
| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Project Split Layout | `agenticdevelopercookbook://ingredients/ui/windows/project-split-layout` | Arranges the panels, owns proportions, visibility, toolbar and persisted ProjectSettings | Yes | Defaults: sessions 15%, file tree 20%, detail split 0.5; inspector hidden |
| File Tree Browser | `agenticdevelopercookbook://ingredients/ui/panels/file-tree-browser` | File tree panel content, selection, and directory sync | Yes | Root = project repository directory |
| Code Editor Pane | `agenticdevelopercookbook://ingredients/ui/panels/code-editor-pane` | Editor content in the top section of the detail area | Yes | Default |
| Terminal Pane | `agenticdevelopercookbook://ingredients/ui/panels/terminal-pane` | Terminal content in the bottom section of the detail area; owns sessions and processes | Yes | Auto-open per user setting |
| Inspector Panel | `agenticdevelopercookbook://ingredients/ui/panels/inspector-panel` | Right-side metadata panel for the selected item | No | Hidden by default; 250pt fixed width |
| Collapsible Pane Header | `agenticdevelopercookbook://ingredients/ui/components/collapsible-pane-header` | Header above the editor and terminal sections that collapses or expands each | Yes | Two instances: "Editor" and "Terminal" |
| Status Bar | `agenticdevelopercookbook://ingredients/ui/components/status-bar` | Sync-status overlay at the bottom of the file tree panel | Yes | Visible only during directory sync |
| Window Frame Persistence | `agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence` | Persists window position and size per project | Yes | Autosave name = SHA256 of the project path |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Per-category logger for window-level events | Yes | Category `ProjectWindow` |
| Settings Keys | `agenticdevelopercookbook://ingredients/infrastructure/settings-keys` | Central registry for the ProjectSettings keys and user-setting keys | No | Keys for the Project Settings table |


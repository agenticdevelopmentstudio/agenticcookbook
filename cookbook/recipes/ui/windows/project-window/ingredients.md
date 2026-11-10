
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Project Split Layout | [adc.ingredient.ui.windows.project-split-layout](cookbook:865679a9-6631-46e8-84ae-6ef64d2abf3a) | Arranges the panels, owns proportions, visibility, toolbar and persisted ProjectSettings | Yes | Defaults: sessions 15%, file tree 20%, detail split 0.5; inspector hidden |
| File Tree Browser | [adc.ingredient.ui.panels.file-tree-browser](cookbook:a1845427-a2cd-4744-96bf-f6c6f2380982) | File tree panel content, selection, and directory sync | Yes | Root = project repository directory |
| Code Editor Pane | [adc.ingredient.ui.panels.code-editor-pane](cookbook:954e559c-e2bf-494c-a37e-de0b88bec89a) | Editor content in the top section of the detail area | Yes | Default |
| Terminal Pane | [adc.ingredient.ui.panels.terminal-pane](cookbook:4a2898cf-34ed-4153-8d06-c795f80c19cd) | Terminal content in the bottom section of the detail area; owns sessions and processes | Yes | Auto-open per user setting |
| Inspector Panel | [adc.ingredient.ui.panels.inspector-panel](cookbook:6af1d30a-c2ee-4a6d-97ec-50c67f01a243) | Right-side metadata panel for the selected item | No | Hidden by default; 250pt fixed width |
| Collapsible Pane Header | [adc.ingredient.ui.components.collapsible-pane-header](cookbook:1dd2111a-eb05-40e4-b469-1aecd79c5863) | Header above the editor and terminal sections that collapses or expands each | Yes | Two instances: "Editor" and "Terminal" |
| Status Bar | [adc.ingredient.ui.components.status-bar](cookbook:22729bee-7ab4-4648-aa5a-2beef067d0c3) | Sync-status overlay at the bottom of the file tree panel | Yes | Visible only during directory sync |
| Window Frame Persistence | [adc.ingredient.infrastructure.window-frame-persistence](cookbook:85d04a9b-5692-4025-a489-eac8bbb14663) | Persists window position and size per project | Yes | Autosave name = SHA256 of the project path |
| Logging | [adc.ingredient.infrastructure.logging](cookbook:7c2049c7-89d9-4135-b657-dbd03cdd19a0) | Per-category logger for window-level events | Yes | Category `ProjectWindow` |
| Settings Keys | [adc.ingredient.infrastructure.settings-keys](cookbook:39676af7-b0b9-48f2-8056-f0c8e8754ffc) | Central registry for the ProjectSettings keys and user-setting keys | No | Keys for the Project Settings table |


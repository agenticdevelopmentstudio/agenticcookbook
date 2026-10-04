
| Term | Definition |
|------|-----------|
| EditorState | An ObservableObject that manages the loaded file content, modification tracking, load state, and save operations for a single file |
| Dirty state | The editor has unsaved modifications — determined by comparing current content to last-saved content |
| loadGeneration | A monotonically increasing counter that forces the SourceEditor to be recreated when a new file is loaded, preventing stale editor state |
| Syntax highlighting | Colorized rendering of source code tokens (keywords, strings, comments, etc.) based on the detected language |
| Minimap | A scaled-down overview of the entire file shown as a narrow column on the trailing edge of the editor |
| Gutter | The column to the left of the editing area that displays line numbers |
| Auto-save | Automatic persistence of modified content when the user switches to a different file |


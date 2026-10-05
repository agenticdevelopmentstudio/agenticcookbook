
The split-view layout at the heart of the IDE-style project window. An HSplitView arranges the sessions panel, file tree panel, and detail panel side by side; the detail panel is itself a VSplitView holding the code editor (top) and terminal (bottom). An optional inspector panel slides in from the right. Each pane's visibility and proportions are persisted per-project. This ingredient owns the arrangement, sizing, toggling, toolbar, and persisted layout state only; the content of each pane is supplied by the panel ingredients the Project Window recipe composes with it.

### Terminology

| Term | Definition |
|------|-----------|
| Sessions panel | The leftmost panel showing a list of sessions for the project |
| File tree panel | The file browser panel displaying the project's directory hierarchy |
| Detail panel | The center/right area containing the editor and terminal in a vertical split |
| Inspector panel | An optional right-side sliding panel showing metadata for the selected item |
| HSplitView | A horizontal split view dividing the window into side-by-side sections |
| VSplitView | A vertical split view dividing the detail panel into top (editor) and bottom (terminal) |
| Proportional sizing | Each pane occupies a fraction of total width, persisted per-project |
| Frame autosave | The platform mechanism for persisting window position and size between sessions |


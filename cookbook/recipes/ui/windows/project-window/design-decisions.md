
**Fixed 2-pane detail layout**: The current spec uses a fixed VSplitView with editor (top) and terminal (bottom). A future version MAY evolve to a flexible N-pane layout supporting arbitrary pane configurations (file editor, terminal sessions, IDE integration panes). When this ships, the spec should be updated to document `PaneType` enum and `PaneLayout` struct.

**File tree default width**: Currently defaulting to 20% (`fileTreeProportion = 0.20`). Some implementations may prefer 40% for better file name readability. This is configurable per-project — the default can be adjusted based on user feedback.


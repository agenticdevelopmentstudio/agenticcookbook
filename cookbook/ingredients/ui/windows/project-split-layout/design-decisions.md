
**Decision**: Fixed 2-pane detail layout. The layout uses a fixed VSplitView with editor (top) and terminal (bottom). A future version MAY evolve to a flexible N-pane layout supporting arbitrary pane configurations (file editor, terminal sessions, IDE integration panes).
**Rationale**: A fixed two-pane detail area is the smallest layout that serves the current panels. When the flexible layout ships, the spec should be updated to document a `PaneType` enum and `PaneLayout` struct.
**Approved**: pending

**Decision**: File tree default width of 20% (`fileTreeProportion = 0.20`). Some implementations may prefer 40% for better file name readability.
**Rationale**: The proportion is configurable per project, so the default can be adjusted from user feedback without changing the layout contract.
**Approved**: pending


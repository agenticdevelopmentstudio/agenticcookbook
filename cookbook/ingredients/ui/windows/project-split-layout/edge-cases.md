
- **All side panels hidden**: If sessions and file tree are both hidden, the detail panel fills the full window width. The toolbar toggle buttons remain accessible to restore them.
- **Window at minimum size with all panels visible**: Panels MUST respect their minimum width constraints. If the window is too narrow to satisfy all minimums simultaneously, the rightmost resizable panel (detail) SHOULD compress first down to its minimum, and the split view SHOULD prevent further shrinking.
- **Very long repo root name**: The folder header SHOULD truncate with trailing ellipsis rather than overflowing.
- **Multiple project windows open**: Each window has its own ProjectSettings and frame autosave identifier. Settings changes in one window MUST NOT affect another.
- **Inspector toggled rapidly**: Animation MUST not stack or glitch. Each toggle SHOULD cancel any in-flight animation and start fresh.
- **visionOS volume placement**: On visionOS, the window renders as a standard window volume. Panel layout is identical but the user cannot resize panes via drag on visionOS — pane proportions are controlled via settings.


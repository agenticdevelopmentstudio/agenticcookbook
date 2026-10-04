
- **All side panels hidden**: If sessions and file tree are both hidden, the detail panel fills the full window width. The toolbar toggle buttons remain accessible to restore them.
- **Both editor and terminal collapsed**: Only the two pane headers are visible stacked vertically. The user can re-expand either by clicking its header.
- **Window at minimum size with all panels visible**: Panels MUST respect their minimum width constraints. If the window is too narrow to satisfy all minimums simultaneously, the rightmost resizable panel (detail) SHOULD compress first down to its minimum, and the split view SHOULD prevent further shrinking.
- **Project path changes (rename/move)**: The window frame autosave identifier is based on the original path's SHA256 hash. If the project is moved, the frame will not restore. This is expected — the window opens at default position for the new path.
- **Very long repo root name**: The folder header SHOULD truncate with trailing ellipsis rather than overflowing.
- **No git repository**: File tree renders without git status badges; inspector omits Git Status row. No error displayed.
- **File watcher fails to start**: The window SHOULD log an error and continue operating without live file updates. A manual refresh mechanism SHOULD be available.
- **Terminal process crashes**: The terminal pane SHOULD display an error state. Other panels MUST remain functional.
- **Multiple project windows open**: Each window has its own ProjectSettings and frame autosave identifier. Settings changes in one window MUST NOT affect another.
- **Inspector toggled rapidly**: Animation MUST not stack or glitch. Each toggle SHOULD cancel any in-flight animation and start fresh.
- **Extremely large project (100k+ files)**: Lazy loading in the file tree (delegated to file-tree-browser) mitigates this. The window itself SHOULD remain responsive.
- **visionOS volume placement**: On visionOS, the window renders as a standard window volume. Panel layout is identical but the user cannot resize panes via drag on visionOS — pane proportions are controlled via settings.


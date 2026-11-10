
- **Both editor and terminal collapsed**: Only the two pane headers are visible stacked vertically. The user can re-expand either by clicking its header.
- **Project path changes (rename/move)**: The window frame autosave identifier is based on the original path's SHA256 hash. If the project is moved, the frame will not restore. This is expected — the window opens at default position for the new path.
- **No git repository**: File tree renders without git status badges; inspector omits Git Status row. No error displayed.
- **File watcher fails to start**: The window SHOULD log an error and continue operating without live file updates. A manual refresh mechanism SHOULD be available.
- **Terminal process crashes**: The terminal pane SHOULD display an error state. Other panels MUST remain functional.
- **Extremely large project (100k+ files)**: Lazy loading in the file tree (delegated to file-tree-browser) mitigates this. The window itself SHOULD remain responsive.


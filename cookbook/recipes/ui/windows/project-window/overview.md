
The primary IDE-style project window that composes multiple sub-components into a four-panel layout. An HSplitView arranges the sessions panel, file tree panel, and detail panel side by side; the detail panel is itself a VSplitView containing the code editor (top) and terminal (bottom). An optional inspector panel slides in from the right. Each pane's visibility and proportions are persisted per-project, and the window frame is auto-saved using a SHA256 hash of the project path.


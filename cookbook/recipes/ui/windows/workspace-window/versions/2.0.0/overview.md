
A two-pane workspace browser window for managing multiple projects. A horizontal split holds the Workspace Browser (sidebar of projects and directories, detail pane or welcome state) and is backed by the Workspace Document, a `.catnip-workspace` package with a SQLite database and a pool of directory watchers that auto-discover `.catnip-proj` packages. The window persists its frame keyed by a hash of the workspace path and persists the sidebar proportion in the workspace document.



The primary IDE-style project window, composed from a split layout and the panels that fill it. The Project Split Layout ingredient arranges a sessions panel, file tree, and a detail area (code editor over terminal) with an optional inspector; the panel ingredients supply each pane's behavior, collapsible pane headers fold the editor and terminal sections, a status bar reports directory sync, and window frame persistence remembers the window per project using a SHA256 hash of the project path. Use this recipe to build the main window of a project-based development tool.


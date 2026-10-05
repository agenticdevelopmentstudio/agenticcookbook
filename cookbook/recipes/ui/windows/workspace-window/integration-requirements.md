
- **hsplit-sidebar-detail**: The window MUST use an `HSplitView` with a sidebar on the left and a detail pane on the right.
- **persist-window-frame**: The window MUST persist its frame (position and size) between sessions using the window frame persistence mechanism described in [window-frame-persistence.md](../../../ingredients/infrastructure/window-frame-persistence.md). The autosave name MUST be derived from a hash of the workspace file path.
- **sidebar-default-30pct**: The sidebar proportion MUST default to `0.3` and MUST be persisted in the workspace document's `settings` table.
- **resizable-min-size**: The window MUST be resizable with a minimum size sufficient to display the sidebar and detail pane without clipping content.
- **browser-bound-to-document**: The Workspace Browser MUST render exclusively from the Workspace Document's entries, discovered projects, and aggregated `isSyncing` state, and MUST NOT read the file system directly.
- **edits-flow-to-document**: Add and remove actions in the browser (context menus, welcome-state buttons) MUST be applied through the Workspace Document so that validation (duplicate and self-referential rejection) and `syncEntries` run before the sidebar updates.
- **sidebar-proportion-via-document**: The sidebar proportion MUST be read from and written to the Workspace Document's `settings` table, not to window-level storage.
- **frame-key-from-path**: The frame autosave name MUST be a hash of the workspace file path so each workspace window restores independently.
- **window-events-logged**: Window open, close, autosave-name, and sidebar-proportion events MUST use the `logging` ingredient with category `WorkspaceWindow`.


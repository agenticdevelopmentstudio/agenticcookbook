
- **Window open while app quits**: The window MUST NOT reopen on next launch, and the saved frame MUST still be available if the user opens it manually (no-auto-reopen, persist-frame-position).
- **Frame restored off-screen**: If the saved frame is on a display that is no longer attached, the window SHOULD open on a visible display at its saved size, honoring the minimum size.
- **Shortcut during category switch**: Triggering the shortcut while the content panel is updating MUST bring the existing window to front without resetting the selected category.
- **Per-document settings open**: The per-document settings sheet MUST NOT be reachable from, or merged into, this window; opening the main settings window MUST NOT dismiss the sheet.


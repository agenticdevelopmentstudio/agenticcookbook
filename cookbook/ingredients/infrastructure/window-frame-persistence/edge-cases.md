
- **Window opens off-screen** (e.g., saved on external monitor now disconnected): AppKit handles this — `setFrameAutosaveName` adjusts to visible screen area.
- **Duplicate autosave names**: Two windows with the same name will interfere. Use unique identifiers.
- **Rapid open/close**: Observer cleanup in deinit prevents leaks.


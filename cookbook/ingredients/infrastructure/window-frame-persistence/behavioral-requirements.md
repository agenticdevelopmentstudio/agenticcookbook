
- **persist-frame-autosave**: The component MUST persist the window's frame (origin + size) across app sessions using `NSWindow.setFrameAutosaveName`.
- **unique-autosave-name**: Each window MUST have a unique autosave name. For document windows, this SHOULD be derived from the document's file path (e.g., SHA256 hash prefix).
- **invisible-background-view**: The component MUST NOT be visible — it renders as an empty `NSView` added as a background.
- **delayed-window-access**: The component MUST access the hosting `NSWindow` via the view hierarchy after a brief delay (next main run loop cycle) to ensure the window exists.
- **on-close-callback**: The component MAY accept an `onClose` callback that fires when the window is closed (via `NSWindow.willCloseNotification`).
- **cleanup-observers**: The component MUST clean up notification observers on deinit.
- **default-first-launch**: On first launch (no saved frame), the window SHOULD use its default position/size defined elsewhere.



An invisible view modifier that persists a window's position and size between sessions using the platform's native frame autosave mechanism. Attached as a background modifier to any window's root content. On macOS, accesses the hosting `NSWindow` and calls `setFrameAutosaveName`. Supports a close callback for cleanup.


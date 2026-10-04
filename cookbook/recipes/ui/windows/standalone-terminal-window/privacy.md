
- **Data collected**: Terminal output is rendered in-memory by SwiftTerm. No terminal content is stored to disk.
- **Storage**: Active profile ID stored in `@AppStorage` (UserDefaults). Window frame position stored via `NSWindow.setFrameAutosaveName` on macOS.
- **Transmission**: None — terminal content never leaves the device.
- **Retention**: Session data exists only for the lifetime of the window. Profile preference persists until changed. Frame position persists until changed or app is uninstalled.


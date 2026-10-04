
- **Data collected**: Panel visibility and proportion preferences per project; window frame position/size
- **Storage**: ProjectSettings persisted on-device only (platform standard persistence). Frame autosave via `NSWindow.setFrameAutosaveName` (on-device).
- **Transmission**: None — no layout data leaves the device
- **Retention**: Persisted until the user changes settings or the project is removed. Frame autosave cleaned up by the OS if the app is uninstalled.



- **SwiftUI (macOS)**: Register `⌘,` via the `Settings` scene (preferred) or the `.commands` modifier with `CommandGroup(replacing: .appSettings)`. For single-instance enforcement, use a `Window` scene with `defaultPosition` and `handlesExternalEvents`. Frame autosave via `SceneStorage` or `WindowGroup(id:)`. For per-document settings, present `ProjectSettingsView` as `.sheet(isPresented:)` from a toolbar gear button.
- **Compose (Windows)**: Use `Window` with `rememberWindowState()` for position and size persistence. Register `Ctrl+,` via `MenuBar` and a keyboard shortcut handler.
- **React/Electron (Desktop)**: Use a `BrowserWindow` with `show: false` initially. Track the instance to prevent duplicates. Register the shortcut via `globalShortcut` or a menu accelerator.


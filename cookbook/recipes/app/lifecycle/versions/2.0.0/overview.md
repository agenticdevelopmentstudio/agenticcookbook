
Pattern for managing desktop and mobile app lifecycle: what happens on startup, how sessions and documents are restored, and how processes are cleaned up on quit. Startup Behavior decides what to do at launch, Session Restore reopens the previous documents, and Child Process Cleanup ends child processes at quit; the recipe wires them in launch and quit order and declares the multi-window scenes for SwiftUI apps. Covers UIKit scene delegates, Android activity lifecycle, and Web page lifecycle in the ingredients. Derived from scratching-post CatnipApp.swift and AppDelegate.swift.

### Terminology

| Term | Definition |
|------|-----------|
| Scene | A SwiftUI construct (`WindowGroup`, `DocumentGroup`, `Window`, `Settings`) that declares a window type the app can display |


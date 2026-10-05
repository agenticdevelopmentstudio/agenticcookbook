
- **macOS (SwiftUI)**: Declare the menu with `Commands { CommandGroup(replacing: .newItem) { ... } }`; each Button calls into the Document Creation Flow (New Project, New Workspace) or the focused window state (New Session). Keep flow code out of the `App` struct so it stays testable.
- **macOS (AppKit)**: Route menu actions through the responder chain; flow actions live on the app delegate or a document controller, and New Session on the window controller.
- **Windows**: Register accelerators for the three commands and route them to the same flow entry points; New Session dispatches to the active window.
- **Compose and React/Web**: Not applicable — this recipe composes native menu bar and document controller behavior; Compose Desktop and Electron apps follow the Windows approach.



- **SwiftUI (macOS)**: Declare the window scene as `WindowGroup(id: "terminal") { StandaloneTerminalView() }`. Set `.frame(minWidth: 600, minHeight: 400)` on the window content. Attach `.background(WindowAccessor(name: "terminal-window", onClose: { sessionManager.terminateAll() }))` for frame persistence and close handling. Read the active profile ID from `@AppStorage("activeProfileId")` and resolve the profile via `TerminalProfile.activeProfile()` with Solarized Dark fallback.
- **SwiftUI (visionOS)**: Same scene structure as macOS. The window opens as a standard visionOS window volume. Frame persistence is not applicable — visionOS manages window placement. Minimum size constraints are respected by the system.
- **Compose**: Declare a `Window` with `rememberWindowState` and a minimum size of 600x400dp. Persist the frame under the fixed key `terminal-window`. Read the active profile from a shared preferences store.
- **React/Web**: Open the terminal view as a route or window with a 600x400px minimum size; persist its frame in `localStorage` under `terminal-window`. Read the active profile ID from `localStorage`.


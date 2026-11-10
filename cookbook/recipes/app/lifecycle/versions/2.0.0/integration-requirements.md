
- **multi-window-scenes** (macOS/SwiftUI): The app MUST support multiple window types via scene declarations (`WindowGroup`, `DocumentGroup`, `Window`, `Settings`).
- **per-type-document-group**: Each document type SHOULD have its own `DocumentGroup` scene with the appropriate content type and file extensions registered.
- **dedicated-settings-scene**: Settings SHOULD use a dedicated `Settings` scene (macOS 14+) or `Window` scene with `.handlesExternalEvents(matching:)` for older macOS versions.
- **commands-modifier**: Custom menu commands SHOULD be applied via the `.commands` modifier on the primary `WindowGroup`.
- **static-scene-declarations**: The `@main` App struct MUST compose all scene declarations in its `body` property. Scene declarations MUST NOT be generated dynamically at runtime.

### Launch and quit wiring

- **mode-gates-restore**: Session Restore MUST run only when the Startup Behavior mode resolves to `restoreSession`; in `newWindow` and `nothing` modes it MUST NOT open any saved document.
- **restore-fallback-uses-new-window**: When Session Restore finds no valid URLs, it MUST hand control back to Startup Behavior's `newWindow` behavior exactly once, so that only one default window opens.
- **save-before-cleanup**: On quit, the app MUST save the Session Restore URL list before Child Process Cleanup begins, so a slow or timed-out cleanup cannot lose the list.
- **keys-through-registry**: The startup mode and the restore URL list MUST be stored under keys declared through the `settings-keys` ingredient.
- **log-lifecycle-events**: All lifecycle events MUST be logged through the `logging` ingredient with category `AppLifecycle`.


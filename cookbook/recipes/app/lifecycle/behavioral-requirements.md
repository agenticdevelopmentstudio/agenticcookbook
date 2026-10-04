
### Startup behavior

- **configurable-startup-modes**: The app MUST support configurable startup behavior with at least the following modes:
  - `newWindow` — open the default window (e.g., new document or welcome screen)
  - `restoreSession` — reopen previously open documents/windows
  - `nothing` — launch silently to the menu bar (macOS) or dock/background without opening any window
- **startup-behavior-setting**: Startup behavior MUST be a user-configurable setting stored via the platform's standard persistence layer (per `settings-window.md` abstract-persistence). The setting key MUST be centralized in the app's settings key constants (per `settings-window.md` centralized-keys).
- **default-restore-session**: The startup behavior setting MUST default to `restoreSession` on first launch (no prior user preference).

### Session restore

- **save-restore-urls**: When startup behavior is `restoreSession`, the app MUST save the list of open document URLs on quit and reopen them on the next launch.
- **url-list-storage**: The URL list SHOULD be stored in `UserDefaults` (or platform equivalent) as an array of path strings, under a centralized settings key.
- **filter-registered-types**: On restore, the app SHOULD filter saved URLs to only include files whose extensions match the app's registered document types. Unrecognized extensions MUST be silently skipped.
- **validate-file-exists**: On restore, the app MUST validate that each saved URL points to an existing file. Missing files MUST be silently skipped and removed from the saved list.
- **preserve-restore-order**: On restore, the app SHOULD open documents in the same order they were saved (matching the order they were open at quit time).
- **fallback-to-new-window**: If no saved URLs exist (first launch in `restoreSession` mode, or all saved URLs are invalid), the app SHOULD fall back to the `newWindow` behavior.

### Process cleanup

- **terminate-child-processes**: On app termination, the app MUST terminate all child processes (terminal sessions, background tasks, language servers, build processes).
- **sighup-process-group** (macOS): The app SHOULD send `SIGHUP` to its process group on `applicationWillTerminate` to ensure child processes receive a termination signal.
- **track-child-handles**: The app MUST NOT leave orphaned processes after quitting. All child process handles MUST be tracked and cleaned up.
- **cleanup-timeout-sigkill**: Child process cleanup MUST complete within a reasonable timeout (5 seconds). After the timeout, remaining processes SHOULD be sent `SIGKILL`.

### Untitled window suppression

- **suppress-untitled-file** (macOS): `applicationShouldOpenUntitledFile(_:)` MUST return `false` when startup behavior is `nothing` or `restoreSession`.
- **allow-untitled-new-window** (macOS): `applicationShouldOpenUntitledFile(_:)` MUST return `true` when startup behavior is `newWindow`.
- **suppress-untitled-relaunch** (macOS): This method MUST also return `false` when the app is being relaunched by the system after a logout/restart and `restoreSession` is active, to avoid duplicating restored windows with an additional untitled window.

### Multi-window scene wiring

- **multi-window-scenes** (macOS/SwiftUI): The app MUST support multiple window types via scene declarations (`WindowGroup`, `DocumentGroup`, `Window`, `Settings`).
- **per-type-document-group**: Each document type SHOULD have its own `DocumentGroup` scene with the appropriate content type and file extensions registered.
- **dedicated-settings-scene**: Settings SHOULD use a dedicated `Settings` scene (macOS 14+) or `Window` scene with `.handlesExternalEvents(matching:)` for older macOS versions.
- **commands-modifier**: Custom menu commands SHOULD be applied via the `.commands` modifier on the primary `WindowGroup`.
- **static-scene-declarations**: The `@main` App struct MUST compose all scene declarations in its `body` property. Scene declarations MUST NOT be generated dynamically at runtime.


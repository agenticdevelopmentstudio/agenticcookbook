
### Startup behavior

- **configurable-startup-modes**: The app MUST support configurable startup behavior with at least the following modes:
  - `newWindow` — open the default window (e.g., new document or welcome screen)
  - `restoreSession` — reopen previously open documents/windows
  - `nothing` — launch silently to the menu bar (macOS) or dock/background without opening any window
- **startup-behavior-setting**: Startup behavior MUST be a user-configurable setting stored via the platform's standard persistence layer (per the `abstract-persistence` requirement of the `settings-category-browser` ingredient). The setting key MUST be centralized in the app's settings key constants (per the `centralized-keys` requirement of the Settings Window recipe).
- **default-restore-session**: The startup behavior setting MUST default to `restoreSession` on first launch (no prior user preference).

### Untitled window suppression

- **suppress-untitled-file** (macOS): `applicationShouldOpenUntitledFile(_:)` MUST return `false` when startup behavior is `nothing` or `restoreSession`.
- **allow-untitled-new-window** (macOS): `applicationShouldOpenUntitledFile(_:)` MUST return `true` when startup behavior is `newWindow`.
- **suppress-untitled-relaunch** (macOS): This method MUST also return `false` when the app is being relaunched by the system after a logout/restart and `restoreSession` is active, to avoid duplicating restored windows with an additional untitled window.


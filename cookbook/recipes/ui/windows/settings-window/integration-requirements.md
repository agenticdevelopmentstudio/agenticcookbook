
- **platform-keyboard-open**: The window MUST open via the platform-standard keyboard shortcut:
  - macOS: `⌘,` from the app menu (app name menu), labeled "Settings…" (macOS 13+) or "Preferences…" (older)
  - Windows: `Ctrl+,` from the File menu, labeled "Settings"
  - Linux: from the Edit or app menu, labeled "Preferences"
- **single-instance-enforce**: The app MUST enforce single-instance — if the shortcut is triggered while the window is open, the existing window MUST be brought to front. A second instance MUST NOT be created.
- **non-modal-window**: The window MUST be non-modal — it MUST NOT block interaction with other app windows.
- **no-auto-reopen**: The window MUST NOT reopen automatically on app launch, even if it was open when the app was last quit.
- **persist-frame-position**: The window MUST remember its size and position between sessions using the platform's standard frame autosave mechanism.
- **resizable-min-size**: The window MUST be resizable with a minimum size of 500×400pt.
- **centralized-keys**: Settings keys MUST be centralized in an enum or struct of static constants (e.g., `SettingsKeys.general.startupBehavior`). This prevents key duplication and typos across the app.
- **per-document-settings**: Apps with documents or projects SHOULD support per-document settings in addition to app-wide settings. Per-document settings MUST be presented as a sheet (not mixed into the main settings window), typically triggered by a toolbar gear button.
- **browser-fills-window**: The Settings Category Browser MUST fill the window content area, and the window MUST NOT add controls outside it, so the window stays free of Apply or Save buttons.
- **keys-through-registry**: The browser's persistence layer MUST read and write setting keys declared through the `settings-keys` ingredient.
- **frame-through-ingredient**: Frame saving and restoring MUST be performed by the `window-frame-persistence` ingredient, keyed to the settings window, and MUST NOT depend on any category selection.
- **log-window-events**: Window open, front, close, and frame-saved events MUST use the `logging` ingredient with category `SettingsWindow`.


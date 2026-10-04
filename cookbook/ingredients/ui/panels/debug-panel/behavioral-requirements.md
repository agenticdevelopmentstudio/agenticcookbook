
### Access

- **debug-build-only**: The debug panel MUST only be accessible in debug/development builds. It MUST NOT be compiled into release builds.
- **platform-access-gesture**: The debug panel MUST be accessible via a platform-appropriate gesture or action:
  - iOS: Shake gesture
  - macOS: Menu item (Debug menu) or keyboard shortcut `⌘⇧D`
  - watchOS: Force-press or long-press on app icon
  - tvOS: Button sequence on remote (e.g., Play/Pause ×3)
  - visionOS: Long-press on a hidden debug zone
  - Android: Shake gesture or long-press on app version in settings
  - Web: `/debug` route or `Ctrl+Shift+D`

### Feature Flags tab

- **display-flag-states**: MUST display all registered feature flags with their current state (enabled/disabled).
- **flag-toggle-persist**: Each flag MUST be toggleable. Overrides MUST persist across app restarts (stored locally).
- **reset-all-flags**: MUST provide a "Reset All" action that clears all overrides and returns to default/remote values.
- **flag-row-details**: Each flag row MUST show: flag key, current value (on/off), source (default / remote / override).

### Analytics Event Log tab

- **live-event-log**: MUST display a live, scrollable list of analytics events as they are tracked.
- **event-row-details**: Each event row MUST show: timestamp, event name, and properties (expandable).
- **clear-event-log**: MUST provide a "Clear" action to reset the event log.
- **event-log-ephemeral**: The event log MUST be in-memory only — it does not persist across app restarts.

### A/B Test Variants tab

- **display-experiments**: MUST display all registered experiments with their current variant assignment.
- **manual-variant-picker**: Each experiment MUST allow manual variant selection from a picker showing all possible variants.
- **variant-override-persist**: Manual overrides MUST persist across app restarts (stored locally).
- **reset-all-variants**: MUST provide a "Reset All" action that clears overrides and returns to default/remote assignments.

### Backend Configuration tab

- **environment-presets**: MUST allow switching between environment presets: Local, Staging, Production.
- **environment-url-update**: Switching environments MUST update the base URLs for feature flags, analytics, and experiment services.
- **display-backend-urls**: MUST display the current backend URL for each service.
- **custom-url-entry**: Custom URL entry SHOULD be supported for ad-hoc testing.

### Environment Info tab

- **display-env-info**: MUST display: app name, version, build number, OS name and version, device model, screen size/resolution.
- **copy-env-info**: MUST provide a "Copy All" action that copies environment info to the clipboard.

### General

- **modal-presentation**: The debug panel MUST be presented modally (sheet on iOS, floating window on macOS, overlay on Android/Web) and MUST NOT interfere with the app's navigation state.
- **immediate-effect**: Changes made in the debug panel MUST take effect immediately — no restart required.


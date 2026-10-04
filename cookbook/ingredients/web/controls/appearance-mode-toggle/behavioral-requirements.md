
### Mode cycling

- **three-mode-cycle**: The button MUST cycle through exactly three modes in this order: `auto` -> `dark` -> `light` -> `auto`.
- **default-is-auto**: When no forced mode is found in site settings, the control MUST default to `auto`.
- **single-click-advance**: Each click MUST advance to the next mode in the cycle. No long-press, no submenu.

### System theme tracking

- **always-on-listener**: The implementation MUST attach a `matchMedia('(prefers-color-scheme: dark)')` change listener on mount that runs **regardless of the current mode**. This listener updates a cached `systemTheme` state variable whenever the OS appearance changes.
- **no-on-demand-query**: The implementation MUST NOT call `matchMedia().matches` at toggle time to determine the system appearance. On-demand queries return stale or incorrect values in some browsers/frameworks. Instead, the implementation MUST read from the cached `systemTheme` state that the always-on listener keeps current.
- **system-theme-init**: On initialization, read `matchMedia('(prefers-color-scheme: dark)').matches` once to set the initial `systemTheme` value. After that, only the listener updates it.

### Automatic mode

- **auto-follows-system**: In `auto` mode, the resolved appearance MUST equal the cached `systemTheme` value.
- **auto-updates-live**: When the OS appearance changes while in `auto` mode, the page MUST update immediately (the always-on listener updates `systemTheme`, which changes the resolved appearance).
- **auto-clears-setting**: When the user switches to `auto` mode, the appearance mode value MUST be cleared from site settings — not set to `"auto"`. Absence of the value means automatic.
- **auto-instant-switch**: Switching to `auto` MUST apply the correct appearance instantly — no visible flash or delay. The resolved appearance comes from the already-cached `systemTheme`, so no query is needed.

### Forced modes

- **dark-forces-dark**: In `dark` mode, the resolved appearance MUST be dark regardless of the system setting.
- **light-forces-light**: In `light` mode, the resolved appearance MUST be light regardless of the system setting.
- **forced-persists**: When in `dark` or `light` mode, the value MUST be saved to site settings so it survives page reloads and new sessions.
- **forced-ignores-system**: In forced mode, system appearance changes MUST NOT affect the resolved appearance (but the always-on listener still updates `systemTheme` silently, so switching back to auto later is instant).

### Persistence

- **read-on-init**: On initialization, the control MUST read the appearance mode from site settings. If a forced mode value is found (`dark` or `light`), use it. If no value is found, default to `auto`.
- **no-auto-in-storage**: The value `"auto"` MUST NOT be written to site settings. Auto is represented by the absence of a stored value. If `"auto"` is found in storage, it MUST be treated as absence (default to auto) — not as a valid stored mode.
- **clear-on-auto**: Switching to `auto` MUST remove/clear the stored value from site settings, not write `"auto"`.
- **settings-try-catch**: All reads and writes to site settings MUST be wrapped in error handling (e.g., try/catch). If settings are unavailable (private browsing, quota exceeded), the control MUST default to auto and degrade gracefully without showing errors.

### Synchronous class application

- **sync-on-toggle**: When the user clicks the toggle, the CSS class (e.g., `dark` on `<html>`) MUST be applied synchronously — before the framework re-renders. This prevents a visible flash between the old and new appearance. Do NOT rely on a state change triggering a separate effect to update the class; apply it in the same function that handles the click.
- **sync-on-system-change**: When the always-on listener fires a system appearance change (and the mode is `auto`), the CSS class MUST also be applied synchronously in the listener callback, not deferred to an effect.


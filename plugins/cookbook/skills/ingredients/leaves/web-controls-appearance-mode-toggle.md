<!-- leaf: ingredients/web-controls-appearance-mode-toggle · source: ingredients/web/controls/appearance-mode-toggle.md -->

**Rules** (cite as `ingredients/web-controls-appearance-mode-toggle#<slug>`):

- `three-mode-cycle` MUST
- `default-is-auto` MUST
- `single-click-advance` MUST
- `always-on-listener` MUST
- `no-on-demand-query` MUST
- `auto-follows-system` MUST
- `auto-updates-live` MUST
- `auto-clears-setting` MUST
- `auto-instant-switch` MUST
- `dark-forces-dark` MUST
- `light-forces-light` MUST
- `forced-persists` MUST
- `forced-ignores-system` MUST
- `read-on-init` MUST
- `no-auto-in-storage` MUST
- `clear-on-auto` MUST
- `settings-try-catch` MUST
- `sync-on-toggle` MUST
- `sync-on-system-change` MUST
- `dark-mode-icon` MUST
- `light-mode-icon` MUST
- `auto-mode-icon-base` MUST
- `auto-mode-indicator` MUST
- `auto-indicator-no-full-overlay` MUST
- `icon-size-consistent` MUST
- `button-role` MUST
- `aria-label-descriptive` MUST
- `tooltip-descriptive` MUST
- `no-color-only` MUST
- `focus-ring` MUST
- `no-fouc` MUST
- `transmission` MUST — The appearance preference MUST NOT be transmitted to analytics, crash reporting, or any external service.

# Appearance Mode Toggle

## Overview

A three-mode toggle button that cycles between automatic, forced dark, and forced light appearance modes. Automatic mode (the default) follows the operating system's appearance setting in real time. The two forced modes override the system preference.

This recipe is intentionally agnostic about how site settings are stored. The consuming site provides its own persistence mechanism ("site settings") — localStorage, cookies, a database, or any other store. The recipe specifies what to read, write, and clear, but not where.

## Terminology

| Term | Definition |
|------|-----------|
| Appearance mode | One of three values: `auto`, `dark`, `light` |
| System appearance | The OS-level dark/light preference reported by `prefers-color-scheme` |
| Resolved appearance | The actual dark or light appearance applied to the page — either from the system (auto) or from the forced mode |
| Site settings | The consuming site's persistence mechanism for user preferences (not specified by this recipe) |
| Forced mode | Either `dark` or `light` — an explicit override of the system appearance |
| System theme state | A cached copy of the current system appearance, kept in sync by an always-on listener |

## Assumptions

- **site-settings-exist**: The site has a mechanism for storing user settings. This recipe does not specify what that mechanism is — only what values to store and when to clear them.
- **css-class-driven**: The site applies appearance via a CSS class (e.g., `dark` on `<html>`) or equivalent mechanism. This recipe does not specify the CSS architecture.

## Behavioral Requirements

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

## Icons

- **dark-mode-icon**: The forced dark mode MUST display a moon icon.
- **light-mode-icon**: The forced light mode MUST display a sun icon.
- **auto-mode-icon-base**: In `auto` mode, the icon MUST be the same sun or moon icon that matches the current system appearance (moon if system is dark, sun if system is light).
- **auto-mode-indicator**: In `auto` mode, a small sync/refresh badge (circular arrows) MUST appear in the bottom-right corner of the button, overlapping the base icon slightly. The badge MUST be roughly half the size of the base icon (e.g., if the icon is 20px, the badge is ~10px). It MUST be tinted in the site's highlight/accent color. The base icon underneath MUST remain fully visible and unchanged — the badge is a corner annotation, not a full overlay.
- **auto-indicator-no-full-overlay**: The auto indicator MUST NOT be rendered at the same size as the base icon or centered over it. A full-size overlay obscures the sun/moon and makes the mode unreadable. The indicator is a small corner badge only.
- **icon-size-consistent**: All three modes MUST render their base icons at the same size. The auto indicator badge MUST NOT cause the button to grow or shift layout.

## Appearance

- **Button**: Icon-only button, no visible border or background in default state
- **Icon size**: Match the site's standard icon size for header controls
- **Hover**: Text/icon transitions to primary color
- **Auto indicator**: Small badge (~half icon size) in the bottom-right corner, accent/highlight color, not a full overlay

## Accessibility

- **button-role**: The control MUST be a `<button>` element (not a link or div).
- **aria-label-descriptive**: The `aria-label` MUST describe the current mode and what clicking will do. Examples:
  - Auto mode: `"Theme: Auto (currently dark). Click to switch to dark."`
  - Dark mode: `"Theme: Dark. Click to switch to light."`
  - Light mode: `"Theme: Light. Click to switch to auto."`
- **tooltip-descriptive**: The `title` attribute MUST describe the current state:
  - Auto: `"Following system (dark)"` or `"Following system (light)"`
  - Dark: `"Dark mode — click for light"`
  - Light: `"Light mode — click for auto"`
- **no-color-only**: The mode MUST NOT be conveyed by color alone. The icon shape (sun vs moon) and the presence/absence of the badge indicator distinguish the three modes.
- **focus-ring**: The button MUST show a visible focus ring when focused via keyboard (`focus-visible`). Use the site's accent color for the ring.

## Flash Prevention

- **no-fouc**: The page MUST NOT flash the wrong appearance on load. An inline `<script>` in `<head>` (before any stylesheet or framework code) MUST read the stored forced mode from site settings and apply the appropriate CSS class to `<html>` synchronously. If no forced mode is stored, it MUST check `prefers-color-scheme` and apply the matching class. This script MUST be wrapped in try/catch so a settings read failure defaults to no class (light mode).

## Architecture

The implementation consists of three layers:

### 1. Inline script (`<head>`)

Runs before any CSS or JS framework loads. Reads the forced mode from site settings, applies the `dark` class if needed. Prevents FOUC.

### 2. System theme tracker (always-on)

A `matchMedia` listener that runs from mount until unmount, regardless of mode. It maintains a `systemTheme` state variable (`'dark'` or `'light'`). This is the single source of truth for what the OS is currently set to.

### 3. Mode state + resolver

The `mode` state (`'auto'` | `'dark'` | `'light'`) determines which appearance to apply:
- `auto` → use `systemTheme`
- `dark` → use `'dark'`
- `light` → use `'light'`

The resolved theme is a derived value, not independent state. When `mode` or `systemTheme` changes, the resolved theme updates automatically.

```
matchMedia listener ──► systemTheme (always current)
                              │
mode === 'auto' ──────────────┤──► resolved = systemTheme
mode === 'dark' ──────────────┤──► resolved = 'dark'
mode === 'light' ─────────────┘──► resolved = 'light'
                                        │
                                        ▼
                              document.classList.toggle('dark')
```

## Configuration

This ingredient has no configurable options.

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Icon transitions use instant swap instead of animated transition (`motion-reduce:transition-none` in Tailwind) |
| Increase Contrast | Icon uses higher-contrast colors for visibility |
| Forced Colors | Icon rendered in system `ButtonText` color; badge uses `Highlight` |

## Privacy

- **Data collected**: Appearance mode preference only (`dark` or `light`). No value stored for auto (the default).
- **Storage**: Site settings (implementation-defined by the consuming site).
- **Transmission**: The appearance preference MUST NOT be transmitted to analytics, crash reporting, or any external service.
- **Retention**: Persists until the user changes it or clears site settings.


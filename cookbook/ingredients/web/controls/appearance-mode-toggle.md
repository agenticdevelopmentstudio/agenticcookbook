---
id: e01e2c5f-32fd-49e3-8f2a-1f64411160cb
title: "Appearance Mode Toggle"
domain: agenticdevelopercookbook://ingredients/web/controls/appearance-mode-toggle
type: ingredient
version: 1.2.0
status: accepted
language: en
created: 2026-03-30
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Three-mode toggle button cycling automatic, forced dark, and forced light appearance. Automatic follows the system and is the default."
platforms:
  - web
  - typescript
tags:
  - appearance-mode-toggle
  - controls
  - dark-mode
  - web
depends-on: []
related: []
references:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme
  - https://web.dev/articles/color-scheme
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Appearance Mode Toggle

## Overview

A three-mode toggle button that cycles between automatic, forced dark, and forced light appearance modes. Automatic mode (the default) follows the operating system's appearance setting in real time. The two forced modes override the system preference.

This recipe is intentionally agnostic about how site settings are stored. The consuming site provides its own persistence mechanism ("site settings") — localStorage, cookies, a database, or any other store. The recipe specifies what to read, write, and clear, but not where.

### Terminology

| Term | Definition |
|------|-----------|
| Appearance mode | One of three values: `auto`, `dark`, `light` |
| System appearance | The OS-level dark/light preference reported by `prefers-color-scheme` |
| Resolved appearance | The actual dark or light appearance applied to the page — either from the system (auto) or from the forced mode |
| Site settings | The consuming site's persistence mechanism for user preferences (not specified by this recipe) |
| Forced mode | Either `dark` or `light` — an explicit override of the system appearance |
| System theme state | A cached copy of the current system appearance, kept in sync by an always-on listener |

### Assumptions

- **site-settings-exist**: The site has a mechanism for storing user settings. This recipe does not specify what that mechanism is — only what values to store and when to clear them.
- **css-class-driven**: The site applies appearance via a CSS class (e.g., `dark` on `<html>`) or equivalent mechanism. This recipe does not specify the CSS architecture.

### Architecture

The implementation consists of three layers:

#### 1. Inline script (`<head>`)

Runs before any CSS or JS framework loads. Reads the forced mode from site settings, applies the `dark` class if needed. Prevents FOUC.

#### 2. System theme tracker (always-on)

A `matchMedia` listener that runs from mount until unmount, regardless of mode. It maintains a `systemTheme` state variable (`'dark'` or `'light'`). This is the single source of truth for what the OS is currently set to.

#### 3. Mode state + resolver

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

### Flash Prevention

- **no-fouc**: The page MUST NOT flash the wrong appearance on load. An inline `<script>` in `<head>` (before any stylesheet or framework code) MUST read the stored forced mode from site settings and apply the appropriate CSS class to `<html>` synchronously. If no forced mode is stored, it MUST check `prefers-color-scheme` and apply the matching class. This script MUST be wrapped in try/catch so a settings read failure defaults to no class (light mode).

## Appearance

- **Button**: Icon-only button, no visible border or background in default state
- **Icon size**: Match the site's standard icon size for header controls
- **Hover**: Text/icon transitions to primary color
- **Auto indicator**: Small badge (~half icon size) in the bottom-right corner, accent/highlight color, not a full overlay

### Icons

- **dark-mode-icon**: The forced dark mode MUST display a moon icon.
- **light-mode-icon**: The forced light mode MUST display a sun icon.
- **auto-mode-icon-base**: In `auto` mode, the icon MUST be the same sun or moon icon that matches the current system appearance (moon if system is dark, sun if system is light).
- **auto-mode-indicator**: In `auto` mode, a small sync/refresh badge (circular arrows) MUST appear in the bottom-right corner of the button, overlapping the base icon slightly. The badge MUST be roughly half the size of the base icon (e.g., if the icon is 20px, the badge is ~10px). It MUST be tinted in the site's highlight/accent color. The base icon underneath MUST remain fully visible and unchanged — the badge is a corner annotation, not a full overlay.
- **auto-indicator-no-full-overlay**: The auto indicator MUST NOT be rendered at the same size as the base icon or centered over it. A full-size overlay obscures the sun/moon and makes the mode unreadable. The indicator is a small corner badge only.
- **icon-size-consistent**: All three modes MUST render their base icons at the same size. The auto indicator badge MUST NOT cause the button to grow or shift layout.

## States

| State | Appearance |
|-------|-----------|
| Auto (system dark) | Moon icon with small accent-colored sync arrows badge in bottom-right corner |
| Auto (system light) | Sun icon with small accent-colored sync arrows badge in bottom-right corner |
| Forced dark | Moon icon (no badge) |
| Forced light | Sun icon (no badge) |
| Hover | Icon transitions to primary text color |
| Focused | Standard focus ring via `focus-visible` |

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

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| amt-001 | default-is-auto | Fresh visit, no stored setting | Mode is auto, appearance matches system |
| amt-002 | three-mode-cycle | Click three times from auto | auto -> dark -> light -> auto |
| amt-003 | auto-clears-setting | Switch from dark to light to auto | Site settings has no appearance mode value |
| amt-004 | forced-persists | Set to dark, reload page | Mode is dark, appearance is dark regardless of system |
| amt-005 | auto-updates-live | In auto mode, change system from light to dark | Page appearance changes to dark without reload |
| amt-006 | auto-instant-switch | System is dark, user sets light, then clicks back to auto | Appearance becomes dark instantly (reads cached systemTheme) |
| amt-007 | forced-ignores-system | In forced light mode, change system to dark | Page remains light |
| amt-008 | no-fouc | Forced dark stored, full page load | No flash of light mode before dark applies |
| amt-009 | auto-mode-icon-base | Auto mode, system is dark | Moon icon displayed with small corner badge |
| amt-010 | auto-mode-icon-base | Auto mode, system is light | Sun icon displayed with small corner badge |
| amt-011 | icon-size-consistent | Toggle through all three modes | Button size does not change |
| amt-012 | no-auto-in-storage | Toggle to auto | String "auto" is NOT in site settings |
| amt-013 | aria-label-descriptive | In dark mode, inspect button | aria-label includes "Dark" and describes next mode |
| amt-014 | sync-on-toggle | Click toggle from light to auto (system is dark) | No visible flash of light before dark applies |
| amt-015 | no-on-demand-query | Toggle to auto | Implementation reads cached systemTheme, does not call matchMedia().matches |
| amt-016 | settings-try-catch | localStorage disabled, toggle modes | No errors thrown, defaults to auto |
| amt-017 | focus-ring | Tab to button | Visible accent-colored focus ring appears |
| amt-018 | always-on-listener | In forced dark mode, system changes to light, then toggle to auto | Page shows light (listener was tracking system change even in forced mode) |

## Edge Cases

- **Settings unavailable**: If site settings cannot be read (e.g., storage quota exceeded, cookies disabled), the control MUST default to auto mode and degrade gracefully — no errors shown to the user. All settings access MUST be wrapped in try/catch.
- **System appearance undefined**: If `prefers-color-scheme` is not supported by the browser, auto mode MUST default to light.
- **Rapid clicking**: Rapid toggling MUST NOT cause visual glitches or inconsistent state. Each click produces exactly one mode transition.
- **SSR / hydration mismatch**: If the page is server-rendered, the inline script in `<head>` handles the initial class. The client-side framework MUST read the same stored value on hydration to avoid a mismatch.
- **Stale matchMedia queries**: Do NOT call `matchMedia().matches` on demand (e.g., in a click handler or effect). Some browsers/frameworks return stale values from on-demand queries. The always-on listener pattern avoids this entirely.
- **Legacy storage migration**: If a previous implementation stored the theme under a different key (e.g., `theme` instead of `theme-mode`), the initialization logic SHOULD detect and migrate it, then remove the old key.

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

## Logging

Subsystem: `{{bundle_id}}` | Category: `AppearanceModeToggle`

| Event | Level | Message |
|-------|-------|---------|
| Mode changed | debug | `AppearanceModeToggle: mode changed to {{mode}}` |
| System theme detected | debug | `AppearanceModeToggle: system theme is {{theme}}` |
| Preference persisted | debug | `AppearanceModeToggle: saved preference {{mode}} to localStorage` |

## Platform Notes

- **React**: Implement as a context provider (`ThemeProvider`) with a `useTheme()` hook exposing `mode` (`auto`/`dark`/`light`), `theme` (resolved `dark`/`light`), and `toggle()`. Track `systemTheme` as state with a `useEffect` that attaches the `matchMedia` listener on mount (no dependencies — always runs). Derive `theme` from `mode` and `systemTheme` (not as independent state). In `toggle()`, apply the CSS class synchronously before calling `setMode()`. The `matchMedia` query object should be created once at module scope, not inside effects.
- **Vue**: Implement as a composable (`useTheme()`) with reactive `mode`, `systemTheme`, and computed `theme` refs. Attach `matchMedia` listener in `onMounted`. Apply class synchronously in the toggle function.
- **Vanilla JS**: Create the `matchMedia` object once. Attach listener immediately. Store `systemTheme` in a module-level variable. `toggle()` reads from this variable for auto resolution. Apply class synchronously.
- **CSS**: The toggle applies a class (e.g., `dark`) to `<html>`. All theme-aware styles use CSS custom properties scoped to the presence/absence of that class. Example: `:root { --bg: white; } .dark { --bg: #0c0c0f; }`.

## Design Decisions

### Implementation Anti-Patterns

These patterns were discovered during development and MUST be avoided:

| Anti-pattern | Problem | Correct approach |
|-------------|---------|-----------------|
| On-demand `matchMedia().matches` query in toggle handler | Returns stale values in some browsers/frameworks | Read from cached `systemTheme` state |
| Full-size overlay for auto indicator | Obscures the base sun/moon icon, making the mode unreadable | Small corner badge (~half icon size) |
| Separate `useEffect` for applying CSS class | Causes visible flash — class update waits for re-render | Apply class synchronously in toggle function and listener |
| Writing `"auto"` to storage | Breaks the "absence = auto" convention; interferes with initialization | Remove/clear the stored value |
| Listener only active in auto mode | `systemTheme` is stale when switching back to auto | Always-on listener regardless of mode |
| Relying on `resolveTheme()` function that queries `matchMedia` | Introduces the stale-query bug at every call site | Derive resolved theme from `mode` + `systemTheme` state |

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [contrast-ratio](agenticdevelopercookbook://compliance/accessibility#contrast-ratio) | partial | Accessibility |
| [keyboard-navigable](agenticdevelopercookbook://compliance/accessibility#keyboard-navigable) | partial | Accessibility |
| [platform-theming](agenticdevelopercookbook://compliance/platform-compliance#platform-theming) | partial | Platform |
| [reduced-motion](agenticdevelopercookbook://compliance/accessibility#reduced-motion) | partial | Accessibility |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-30 | Mike Fullerton | Initial creation |
| 1.1.0 | 2026-03-30 | Mike Fullerton | Add always-on listener architecture, synchronous class application, anti-patterns table, architecture diagram, settings error handling, focus ring, 5 new test vectors |
| 1.2.0 | 2026-10-04 | Mike Fullerton | Conform to the ingredient format: section order, non-standard sections folded into allowed ones, Compliance added |

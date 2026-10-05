
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


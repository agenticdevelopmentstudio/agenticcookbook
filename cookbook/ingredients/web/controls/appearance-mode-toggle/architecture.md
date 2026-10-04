
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


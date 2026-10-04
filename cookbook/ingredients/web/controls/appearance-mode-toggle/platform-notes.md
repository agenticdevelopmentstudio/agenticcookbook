
- **React**: Implement as a context provider (`ThemeProvider`) with a `useTheme()` hook exposing `mode` (`auto`/`dark`/`light`), `theme` (resolved `dark`/`light`), and `toggle()`. Track `systemTheme` as state with a `useEffect` that attaches the `matchMedia` listener on mount (no dependencies — always runs). Derive `theme` from `mode` and `systemTheme` (not as independent state). In `toggle()`, apply the CSS class synchronously before calling `setMode()`. The `matchMedia` query object should be created once at module scope, not inside effects.
- **Vue**: Implement as a composable (`useTheme()`) with reactive `mode`, `systemTheme`, and computed `theme` refs. Attach `matchMedia` listener in `onMounted`. Apply class synchronously in the toggle function.
- **Vanilla JS**: Create the `matchMedia` object once. Attach listener immediately. Store `systemTheme` in a module-level variable. `toggle()` reads from this variable for auto resolution. Apply class synchronously.
- **CSS**: The toggle applies a class (e.g., `dark`) to `<html>`. All theme-aware styles use CSS custom properties scoped to the presence/absence of that class. Example: `:root { --bg: white; } .dark { --bg: #0c0c0f; }`.


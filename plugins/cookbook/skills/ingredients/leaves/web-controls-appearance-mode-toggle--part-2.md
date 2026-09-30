<!-- leaf: ingredients/web-controls-appearance-mode-toggle--part-2 · source: ingredients/web/controls/appearance-mode-toggle.md -->

# Appearance Mode Toggle — continued (part 2)

**Rules** (cite as `ingredients/web-controls-appearance-mode-toggle--part-2#<slug>`):

- `discovered-during-development-avoided` MUST — These patterns were discovered during development and MUST be avoided:

## Platform Notes

- **React**: Implement as a context provider (`ThemeProvider`) with a `useTheme()` hook exposing `mode` (`auto`/`dark`/`light`), `theme` (resolved `dark`/`light`), and `toggle()`. Track `systemTheme` as state with a `useEffect` that attaches the `matchMedia` listener on mount (no dependencies — always runs). Derive `theme` from `mode` and `systemTheme` (not as independent state). In `toggle()`, apply the CSS class synchronously before calling `setMode()`. The `matchMedia` query object should be created once at module scope, not inside effects.
- **Vue**: Implement as a composable (`useTheme()`) with reactive `mode`, `systemTheme`, and computed `theme` refs. Attach `matchMedia` listener in `onMounted`. Apply class synchronously in the toggle function.
- **Vanilla JS**: Create the `matchMedia` object once. Attach listener immediately. Store `systemTheme` in a module-level variable. `toggle()` reads from this variable for auto resolution. Apply class synchronously.
- **CSS**: The toggle applies a class (e.g., `dark`) to `<html>`. All theme-aware styles use CSS custom properties scoped to the presence/absence of that class. Example: `:root { --bg: white; } .dark { --bg: #0c0c0f; }`.

## Implementation Anti-Patterns

These patterns were discovered during development and MUST be avoided:

| Anti-pattern | Problem | Correct approach |
|-------------|---------|-----------------|
| On-demand `matchMedia().matches` query in toggle handler | Returns stale values in some browsers/frameworks | Read from cached `systemTheme` state |
| Full-size overlay for auto indicator | Obscures the base sun/moon icon, making the mode unreadable | Small corner badge (~half icon size) |
| Separate `useEffect` for applying CSS class | Causes visible flash — class update waits for re-render | Apply class synchronously in toggle function and listener |
| Writing `"auto"` to storage | Breaks the "absence = auto" convention; interferes with initialization | Remove/clear the stored value |
| Listener only active in auto mode | `systemTheme` is stale when switching back to auto | Always-on listener regardless of mode |
| Relying on `resolveTheme()` function that queries `matchMedia` | Introduces the stale-query bug at every call site | Derive resolved theme from `mode` + `systemTheme` state |


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


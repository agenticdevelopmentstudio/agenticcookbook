
- `should-not-replace-text-with-icons`: every icon supplements text, except universally understood symbols (play, pause, close, search), or the code says why
- `should-use-native-icon-set-first`: every icon comes from the platform's native set (SF Symbols, Material Symbols, Segoe Fluent Icons), or the code says why not
- `must-label-action-icons`: every icon accompanying an action has a text label or accessible name
- `should-keep-icon-size-and-weight-consistent`: icons share one size and weight across the UI, or the code says why not
- `should-not-mix-outlined-and-filled-without-intention`: outlined and filled styles are mixed only where the mix carries meaning (e.g., filled = selected, outlined = unselected)
- `should-meet-minimum-icon-size`: every decorative icon is at least 16x16pt and every interactive icon at least 24x24pt, or the code says why not
- `must-pair-state-icons-with-color-and-shape`: every icon conveying state (error, success, warning) is paired with color and shape

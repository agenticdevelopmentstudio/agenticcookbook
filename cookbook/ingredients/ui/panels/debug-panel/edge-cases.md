
- **No feature flags registered**: Flags tab SHOULD show "No feature flags registered" rather than empty.
- **No experiments registered**: A/B tab SHOULD show "No experiments registered."
- **Analytics log very long**: Event log SHOULD use a virtualized/recycled list. Cap at 1000 events in memory.
- **Backend unreachable after switch**: SHOULD show connection error inline, not crash. Allow switching back.


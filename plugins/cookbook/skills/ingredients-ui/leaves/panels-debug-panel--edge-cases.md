<!-- leaf: ingredients-ui/panels-debug-panel--edge-cases · source: ingredients/ui/panels/debug-panel.md -->

# Debug Panel

**Rules** (cite as `ingredients-ui/panels-debug-panel--edge-cases#<slug>`):

- `no-feature-flags-registered` SHOULD — Flags tab SHOULD show "No feature flags registered" rather than empty.
- `no-experiments-registered` SHOULD — A/B tab SHOULD show "No experiments registered."
- `analytics-log-very-long` SHOULD — Event log SHOULD use a virtualized/recycled list. Cap at 1000 events in memory.
- `backend-unreachable-after-switch` SHOULD — SHOULD show connection error inline, not crash. Allow switching back.

## Edge Cases

- **No feature flags registered**: Flags tab SHOULD show "No feature flags registered" rather than empty.
- **No experiments registered**: A/B tab SHOULD show "No experiments registered."
- **Analytics log very long**: Event log SHOULD use a virtualized/recycled list. Cap at 1000 events in memory.
- **Backend unreachable after switch**: SHOULD show connection error inline, not crash. Allow switching back.

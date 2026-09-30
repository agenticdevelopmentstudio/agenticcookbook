<!-- leaf: ingredients-ui/panels-debug-panel--test-vectors · source: ingredients/ui/panels/debug-panel.md -->

# Debug Panel

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| debug-001 | debug-build-only | Build in Release config, attempt shake gesture | No debug panel appears |
| debug-002 | debug-build-only | Build in Debug config, attempt shake gesture | Debug panel appears |
| debug-003 | flag-toggle-persist | Toggle a flag in debug panel, restart app | Override persists after restart |
| debug-004 | reset-all-flags | Override 3 flags, tap Reset All | All flags return to default/remote values |
| debug-005 | live-event-log | Trigger a user action that tracks an event | Event appears in analytics log with correct name and properties |
| debug-006 | manual-variant-picker | Select a different variant for an experiment | Variant assignment changes immediately |
| debug-007 | environment-presets | Switch from Production to Staging | Backend URLs update to staging values |
| debug-008 | copy-env-info | Tap Copy All on environment info | Clipboard contains formatted environment info |
| debug-009 | immediate-effect | Toggle a feature flag | Feature behavior changes immediately without app restart |

<!-- leaf: ingredients/web-controls-appearance-mode-toggle--test-vectors · source: ingredients/web/controls/appearance-mode-toggle.md -->

# Appearance Mode Toggle

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

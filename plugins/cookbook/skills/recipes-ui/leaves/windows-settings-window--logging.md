<!-- leaf: recipes-ui/windows-settings-window--logging · source: recipes/ui/windows/settings-window.md -->

# Settings Window

## Logging

Subsystem: `{{bundle_id}}` | Category: `SettingsWindow`

| Event | Level | Message |
|-------|-------|---------|
| Window opened | debug | `SettingsWindow: opened` |
| Window brought to front | debug | `SettingsWindow: already open, brought to front` |
| Window closed | debug | `SettingsWindow: closed` |
| Category selected | debug | `SettingsWindow: selected category "{{name}}"` |
| Setting changed | debug | `SettingsWindow: changed "{{key}}" from "{{oldValue}}" to "{{newValue}}"` |
| Frame saved | debug | `SettingsWindow: frame saved ({{x}}, {{y}}, {{width}}×{{height}})` |

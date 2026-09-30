<!-- leaf: ingredients-ui/components-color-profile--logging · source: ingredients/ui/components/color-profile.md -->

# Color Profile

## Logging

Subsystem: `{{bundle_id}}` | Category: `ColorProfile`

| Event | Level | Message |
|-------|-------|---------|
| Active profile changed | debug | `ColorProfile: active profile changed to "{{name}}" ({{id}})` |
| Profile duplicated | debug | `ColorProfile: duplicated "{{source}}" as "{{new}}"` |
| Profile deleted | debug | `ColorProfile: deleted "{{name}}" ({{id}})` |
| Fallback to default | debug | `ColorProfile: invalid active ID, falling back to Solarized Dark` |

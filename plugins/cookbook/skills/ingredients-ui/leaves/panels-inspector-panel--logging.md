<!-- leaf: ingredients-ui/panels-inspector-panel--logging · source: ingredients/ui/panels/inspector-panel.md -->

# Inspector Panel

## Logging

Subsystem: `{{bundle_id}}` | Category: `InspectorPanel`

| Event | Level | Message |
|-------|-------|---------|
| Panel shown | debug | `InspectorPanel: shown` |
| Panel hidden | debug | `InspectorPanel: hidden` |
| Visibility state persisted | debug | `InspectorPanel: visibility persisted as {{visible}}` |
| Item inspected | debug | `InspectorPanel: inspecting "{{name}}" at "{{path}}"` |
| Empty state displayed | debug | `InspectorPanel: no selection, showing empty state` |
| Type detection failed | debug | `InspectorPanel: could not determine type for "{{name}}", showing "Unknown"` |

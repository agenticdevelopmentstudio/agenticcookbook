<!-- leaf: ingredients-ui/panels-ai-settings-panel--states · source: ingredients/ui/panels/ai-settings-panel.md -->

# AI Settings Panel

## States

| State | Behavior |
|-------|----------|
| AI features disabled | Enable toggle is off; all other controls are dimmed and non-interactive |
| AI features enabled, no key | Enable toggle is on; controls are interactive; connection status is "Untested" |
| AI features enabled, key entered | Controls interactive; enable toggle auto-set to on (auto-enable-on-key-entry) |
| Connection testing | Spinner on Test Connection button; status shows previous state until test completes |
| Connected | Green dot, "Connected" label |
| Disconnected | Red dot, "Disconnected" label, error description shown below |
| Provider changed | Model picker updates options; endpoint section shows/hides; connection status resets to "Untested" |
| Dynamic model fetch in progress | Model picker shows current options with a subtle loading indicator |
| Dynamic model fetch failed | Model picker shows hardcoded defaults; debug log emitted |
| Custom model entered | Custom model field value overrides picker selection |
| Invalid URL entered | Inline error below Base URL field; Test Connection button still available |

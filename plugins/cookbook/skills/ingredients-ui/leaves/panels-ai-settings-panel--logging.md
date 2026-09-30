<!-- leaf: ingredients-ui/panels-ai-settings-panel--logging · source: ingredients/ui/panels/ai-settings-panel.md -->

# AI Settings Panel

**Rules** (cite as `ingredients-ui/panels-ai-settings-panel--logging#<slug>`):

- `critical-logging-rule` MUST — API key values MUST NEVER appear in log output at any level. Log messages reference the provider name or key existence, …

## Logging

Subsystem: `{{bundle_id}}` | Category: `AISettingsPanel`

| Event | Level | Message |
|-------|-------|---------|
| Panel opened | debug | `AISettingsPanel: opened` |
| Panel closed | debug | `AISettingsPanel: closed` |
| AI features toggled | debug | `AISettingsPanel: AI features {{enabled\|disabled}}` |
| Provider changed | debug | `AISettingsPanel: provider changed to "{{provider}}"` |
| Model changed | debug | `AISettingsPanel: model changed to "{{model}}"` |
| Custom model set | debug | `AISettingsPanel: custom model set to "{{model}}"` |
| API key stored | debug | `AISettingsPanel: API key stored for "{{provider}}"` |
| API key removed | debug | `AISettingsPanel: API key removed for "{{provider}}"` |
| Connection test started | debug | `AISettingsPanel: connection test started for "{{provider}}"` |
| Connection test succeeded | debug | `AISettingsPanel: connection test succeeded ({{duration}}ms)` |
| Connection test failed | debug | `AISettingsPanel: connection test failed: {{error}}` |
| Dynamic model fetch started | debug | `AISettingsPanel: fetching models from "{{provider}}"` |
| Dynamic model fetch succeeded | debug | `AISettingsPanel: fetched {{count}} models from "{{provider}}"` |
| Dynamic model fetch failed | debug | `AISettingsPanel: model fetch failed for "{{provider}}", using defaults` |
| Endpoint changed | debug | `AISettingsPanel: endpoint changed to "{{url}}"` |
| Timeout changed | debug | `AISettingsPanel: timeout changed to {{seconds}}s` |
| Secure storage error | error | `AISettingsPanel: secure storage unavailable: {{error}}` |
| Insecure key migration | info | `AISettingsPanel: migrated API key from insecure storage to secure storage for "{{provider}}"` |

**Critical logging rule**: API key values MUST NEVER appear in log output at any level. Log messages reference the provider name or key existence, never the key value.


Subsystem: `{{bundle_id}}` | Category: `SettingsKeys`

| Event | Level | Message |
|-------|-------|---------|
| Duplicate key detected | error | `SettingsKeys: duplicate key value "{{key}}" found` |
| Deprecated key accessed | debug | `SettingsKeys: deprecated key "{{key}}" accessed — migration pending` |
| Key migration performed | info | `SettingsKeys: migrated "{{oldKey}}" to "{{newKey}}"` |


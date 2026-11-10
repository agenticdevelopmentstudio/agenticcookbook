
| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Settings Category Browser | `agenticdevelopercookbook://ingredients/ui/windows/settings-category-browser` | Sidebar categories, content panel, immediate apply, persistence abstraction | Yes | Layout variant per app; first category selected by default |
| Window Frame Persistence | `agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence` | Remembers window size and position between sessions | Yes | Minimum size 500x400pt |
| Settings Keys | `agenticdevelopercookbook://ingredients/infrastructure/settings-keys` | Central registry of setting keys | Yes | Keys in an enum or struct of static constants |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Logger for window-level events | Yes | Category `SettingsWindow` |
| Empty State | `agenticdevelopercookbook://ingredients/ui/components/empty-state` | Message shown when no categories are defined | No | Strings `settings.no_categories`, `settings.no_settings` |


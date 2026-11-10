
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Settings Category Browser | [adc.ingredient.ui.windows.settings-category-browser](cookbook:4a047375-7f4f-4bca-84a5-62a0f70fc5c9) | Sidebar categories, content panel, immediate apply, persistence abstraction | Yes | Layout variant per app; first category selected by default |
| Window Frame Persistence | [adc.ingredient.infrastructure.window-frame-persistence](cookbook:85d04a9b-5692-4025-a489-eac8bbb14663) | Remembers window size and position between sessions | Yes | Minimum size 500x400pt |
| Settings Keys | [adc.ingredient.infrastructure.settings-keys](cookbook:39676af7-b0b9-48f2-8056-f0c8e8754ffc) | Central registry of setting keys | Yes | Keys in an enum or struct of static constants |
| Logging | [adc.ingredient.infrastructure.logging](cookbook:7c2049c7-89d9-4135-b657-dbd03cdd19a0) | Logger for window-level events | Yes | Category `SettingsWindow` |
| Empty State | [adc.ingredient.ui.components.empty-state](cookbook:ce2af25c-4f18-41ae-91b9-342e363449b3) | Message shown when no categories are defined | No | Strings `settings.no_categories`, `settings.no_settings` |


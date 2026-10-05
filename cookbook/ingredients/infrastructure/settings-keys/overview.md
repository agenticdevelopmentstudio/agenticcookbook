
A centralized settings key registry that prevents key duplication, typos, and scattered string literals. All UserDefaults/SharedPreferences/localStorage keys are defined in one place with a structured naming convention. Every setting read or written anywhere in the app MUST reference a constant from this registry rather than an inline string. This is the implementation pattern for the `centralized-keys` requirement of the Settings Window recipe (`agenticdevelopercookbook://recipes/ui/windows/settings-window`).

### Terminology

| Term | Definition |
|------|-----------|
| Key | A string constant used to read/write a setting in the platform persistence layer |
| Area | A logical grouping of keys, corresponding to a settings window category |
| Key registry | The single source of truth for all settings key constants |


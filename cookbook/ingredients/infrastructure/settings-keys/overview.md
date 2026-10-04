
A centralized settings key registry that prevents key duplication, typos, and scattered string literals. All UserDefaults/SharedPreferences/localStorage keys are defined in one place with a structured naming convention. Every setting read or written anywhere in the app MUST reference a constant from this registry rather than an inline string. This is the implementation pattern for settings-window.md centralized-keys.


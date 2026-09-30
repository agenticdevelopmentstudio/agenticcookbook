<!-- leaf: ingredients/infrastructure-settings-keys--test-vectors · source: ingredients/infrastructure/settings-keys.md -->

# Settings Keys

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| keys-001 | globally-unique-keys | Collect all key string values from the registry | No duplicate values found |
| keys-002 | dot-notation-naming | Iterate all key string values | Every value matches regex `^[a-z]+\.[a-zA-Z]+$` (area dot camelCase) |
| keys-003 | static-string-constants | Inspect all key declarations | All are static/const, none are computed properties or function calls |
| keys-004 | centralized-key-registry | Search codebase for `UserDefaults.standard.string(forKey:` / `@AppStorage(` / `localStorage.getItem(` | Every call site references a `SettingsKeys` constant, never a string literal |
| keys-005 | lowercase-area-prefix | Extract area prefixes from all keys | Each area prefix matches a settings window category name (lowercase) |
| keys-006 | camelcase-setting-name | Extract setting names (after the dot) from all keys | Each matches camelCase: `^[a-z][a-zA-Z]*$` |
| keys-007 | immutable-shipped-keys | Compare key strings between current release and previous release | No shipped key strings have changed |
| keys-008 | use-registry-constants | Grep for raw string matching `"general.` or `"ai.` in non-registry files | Zero matches outside the key registry file |
| keys-009 | importable-from-modules | Import key registry from a separate module | Import succeeds, constants are accessible |

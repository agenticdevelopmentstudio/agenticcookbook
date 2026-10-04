
### Structure

- **centralized-key-registry**: All settings keys MUST be defined in a centralized struct/enum (e.g., `struct SettingsKeys`). Inline string literals for settings keys MUST NOT appear anywhere else in the codebase.
- **static-string-constants**: Keys MUST be static string constants, NOT computed or dynamically constructed at runtime.
- **dot-notation-naming**: Keys MUST follow a dot-notation naming convention: `{area}.{setting}` (e.g., `general.startupBehavior`, `ai.enabled`, `profiles.activeProfileID`).
- **organize-by-area**: Keys SHOULD be organized by settings area, matching the settings window categories (e.g., all `general.*` keys grouped together, all `ai.*` keys grouped together).

### Naming convention

- **lowercase-area-prefix**: The area prefix MUST match the settings category name in lowercase (e.g., `general`, `ai`, `profiles`).
- **camelcase-setting-name**: The setting name MUST be camelCase (e.g., `startupBehavior`, `apiKey`, `activeProfileID`).
- **globally-unique-keys**: Keys MUST be globally unique within the app. No two keys MAY share the same string value.

### Migration safety

- **immutable-shipped-keys**: Key strings MUST NOT change once shipped in a release build. Changing a shipped key string loses existing user settings for that key.
- **mark-deprecated-keys**: Deprecated keys SHOULD be marked with a comment (e.g., `// Deprecated: migrated to ai.provider in v2.0`) rather than deleted, so that migration code can reference both old and new keys.
- **preserve-key-names-migration**: When migrating storage backend (e.g., UserDefaults to SQLite, localStorage to IndexedDB), the key names SHOULD be preserved to avoid data loss.

### Usage pattern

- **use-registry-constants**: All reads and writes to the persistence layer MUST use a constant from the key registry. Code review SHOULD reject any raw string literal used as a settings key.
- **importable-from-modules**: The key registry MUST be importable from any module that needs to read or write settings.


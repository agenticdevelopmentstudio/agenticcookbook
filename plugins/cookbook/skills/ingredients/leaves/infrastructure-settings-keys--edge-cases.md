<!-- leaf: ingredients/infrastructure-settings-keys--edge-cases · source: ingredients/infrastructure/settings-keys.md -->

# Settings Keys

**Rules** (cite as `ingredients/infrastructure-settings-keys--edge-cases#<slug>`):

- `key-collision` MUST — Two developers independently add a key with the same string value. The uniqueness test (keys-001) MUST catch this at …
- `migration-from-old-keys` MUST — When renaming a key area (e.g., prefs.foo to general.foo), the migration code MUST read the old key, write the new key, …
- `platform-specific-keys` SHOULD — If a key only applies to one platform (e.g., general.defaultShellPath on macOS/Linux only), the constant SHOULD still …
- `empty-or-nil-values` MUST — Reading a key that has never been written MUST return the platform default (nil/null/undefined). Consumers MUST handle …
- `key-with-sensitive-data` SHOULD — Keys storing secrets (e.g., ai.apiKey) SHOULD be documented as sensitive. On Apple platforms, consider Keychain instead …

## Edge Cases

- **Key collision**: Two developers independently add a key with the same string value. The uniqueness test (keys-001) MUST catch this at build or CI time. Implementations SHOULD use a compile-time or test-time assertion to prevent duplicates.
- **Migration from old keys**: When renaming a key area (e.g., `prefs.foo` to `general.foo`), the migration code MUST read the old key, write the new key, and delete the old key — in that order. The old key constant MUST remain in the registry (marked deprecated per mark-deprecated-keys) until the migration window closes.
- **Platform-specific keys**: If a key only applies to one platform (e.g., `general.defaultShellPath` on macOS/Linux only), the constant SHOULD still be defined in the shared registry with a comment noting its platform scope. Platform-specific code MAY choose not to read/write it.
- **Empty or nil values**: Reading a key that has never been written MUST return the platform default (nil/null/undefined). Consumers MUST handle missing values gracefully with fallback defaults.
- **Key with sensitive data**: Keys storing secrets (e.g., `ai.apiKey`) SHOULD be documented as sensitive. On Apple platforms, consider Keychain instead of UserDefaults for such values.

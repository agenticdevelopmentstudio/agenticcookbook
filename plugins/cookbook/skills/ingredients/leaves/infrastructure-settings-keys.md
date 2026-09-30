<!-- leaf: ingredients/infrastructure-settings-keys · source: ingredients/infrastructure/settings-keys.md -->

**Rules** (cite as `ingredients/infrastructure-settings-keys#<slug>`):

- `written-anywhere-app-reference-constant-from-registry` MUST — A centralized settings key registry that prevents key duplication, typos, and scattered string literals. All …
- `centralized-key-registry` MUST
- `static-string-constants` MUST
- `dot-notation-naming` MUST
- `organize-by-area` SHOULD
- `lowercase-area-prefix` MUST
- `camelcase-setting-name` MUST
- `globally-unique-keys` MUST
- `immutable-shipped-keys` MUST
- `mark-deprecated-keys` SHOULD
- `preserve-key-names-migration` SHOULD
- `use-registry-constants` MUST
- `importable-from-modules` MUST

# Settings Keys

## Overview

A centralized settings key registry that prevents key duplication, typos, and scattered string literals. All UserDefaults/SharedPreferences/localStorage keys are defined in one place with a structured naming convention. Every setting read or written anywhere in the app MUST reference a constant from this registry rather than an inline string. This is the implementation pattern for settings-window.md centralized-keys.

## Terminology

| Term | Definition |
|------|-----------|
| Key | A string constant used to read/write a setting in the platform persistence layer |
| Area | A logical grouping of keys, corresponding to a settings window category |
| Key registry | The single source of truth for all settings key constants |

## Behavioral Requirements

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

## Reference Key Set

The following keys are extracted from the scratching-post reference implementation and represent the minimum initial key set:

### general

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `startupBehavior` | `general.startupBehavior` | String | What to show on app launch (e.g., welcome, last project) |
| `defaultShellPath` | `general.defaultShellPath` | String | Path to the default shell executable |
| `newSessionDefault` | `general.newSessionDefault` | String | Default session type for new terminals |
| `reopenProjectsOnLaunch` | `general.reopenProjectsOnLaunch` | Bool | Whether to restore open projects on launch |
| `openProjectURLs` | `general.openProjectURLs` | [String] | List of project URLs to reopen |
| `maxScanWorkers` | `general.maxScanWorkers` | Int | Maximum concurrent file scan workers |

### ai

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `enabled` | `ai.enabled` | Bool | Whether AI features are enabled |
| `provider` | `ai.provider` | String | AI service provider identifier |
| `apiKey` | `ai.apiKey` | String | API key for the AI provider |
| `model` | `ai.model` | String | AI model name/identifier |

### profiles

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `activeProfileID` | `profiles.activeProfileID` | String (UUID) | ID of the currently active color profile |

### settings

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `sidebarWidth` | `settings.sidebarWidth` | Double | Width of the settings window sidebar in points |

## Configuration

This ingredient has no configurable options.

## Platform Notes

- **Swift (Apple)**: Define as `struct SettingsKeys` with nested structs per area, each containing `static let` properties. Example:
  ```swift
  struct SettingsKeys {
      struct General {
          static let startupBehavior = "general.startupBehavior"
          static let defaultShellPath = "general.defaultShellPath"
          // ...
      }
      struct AI {
          static let enabled = "ai.enabled"
          static let provider = "ai.provider"
          // ...
      }
  }
  ```
  Use with `@AppStorage(SettingsKeys.General.startupBehavior)` or `UserDefaults.standard.string(forKey: SettingsKeys.General.startupBehavior)`. For sensitive values like `ai.apiKey`, prefer Keychain Services over UserDefaults.

- **Kotlin (Android)**: Define as `object SettingsKeys` with nested objects per area, each containing `const val` properties. Example:
  ```kotlin
  object SettingsKeys {
      object General {
          const val startupBehavior = "general.startupBehavior"
          const val defaultShellPath = "general.defaultShellPath"
      }
      object AI {
          const val enabled = "ai.enabled"
          const val provider = "ai.provider"
      }
  }
  ```
  Use with `sharedPreferences.getString(SettingsKeys.General.startupBehavior, null)`. For sensitive values, prefer `EncryptedSharedPreferences`.

- **TypeScript (Web)**: Define as a frozen const object with nested objects per area. Example:
  ```typescript
  export const SETTINGS_KEYS = Object.freeze({
      general: {
          startupBehavior: "general.startupBehavior",
          defaultShellPath: "general.defaultShellPath",
      },
      ai: {
          enabled: "ai.enabled",
          provider: "ai.provider",
      },
  } as const);
  ```
  Use with `localStorage.getItem(SETTINGS_KEYS.general.startupBehavior)`. Enforce with an ESLint rule that disallows raw string arguments to `localStorage.getItem`/`setItem`.


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


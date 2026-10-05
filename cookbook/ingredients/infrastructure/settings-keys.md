---
id: 39676af7-b0b9-48f2-8056-f0c8e8754ffc
title: "Settings Keys"
domain: agenticdevelopercookbook://ingredients/infrastructure/settings-keys
type: ingredient
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Centralized settings key registry with dot-notation naming to prevent key duplication and scattered string literals"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
tags:
  - infrastructure
  - settings-keys
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Settings Keys

## Overview

A centralized settings key registry that prevents key duplication, typos, and scattered string literals. All UserDefaults/SharedPreferences/localStorage keys are defined in one place with a structured naming convention. Every setting read or written anywhere in the app MUST reference a constant from this registry rather than an inline string. This is the implementation pattern for the `centralized-keys` requirement of the Settings Window recipe (`agenticdevelopercookbook://recipes/ui/windows/settings-window`).

### Terminology

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

## Appearance

Not applicable — this is a data pattern, not a visual component.

## States

Not applicable — keys are static constants with no runtime state.

## Accessibility

Not applicable — this component has no visual or interactive surface.

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

## Edge Cases

- **Key collision**: Two developers independently add a key with the same string value. The uniqueness test (keys-001) MUST catch this at build or CI time. Implementations SHOULD use a compile-time or test-time assertion to prevent duplicates.
- **Migration from old keys**: When renaming a key area (e.g., `prefs.foo` to `general.foo`), the migration code MUST read the old key, write the new key, and delete the old key — in that order. The old key constant MUST remain in the registry (marked deprecated per mark-deprecated-keys) until the migration window closes.
- **Platform-specific keys**: If a key only applies to one platform (e.g., `general.defaultShellPath` on macOS/Linux only), the constant SHOULD still be defined in the shared registry with a comment noting its platform scope. Platform-specific code MAY choose not to read/write it.
- **Empty or nil values**: Reading a key that has never been written MUST return the platform default (nil/null/undefined). Consumers MUST handle missing values gracefully with fallback defaults.
- **Key with sensitive data**: Keys storing secrets (e.g., `ai.apiKey`) SHOULD be documented as sensitive. On Apple platforms, consider Keychain instead of UserDefaults for such values.

## Configuration

This ingredient has no configurable options.

### Reference Key Set

The following keys are extracted from the scratching-post reference implementation and represent the minimum initial key set:

#### general

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `startupBehavior` | `general.startupBehavior` | String | What to show on app launch (e.g., welcome, last project) |
| `defaultShellPath` | `general.defaultShellPath` | String | Path to the default shell executable |
| `newSessionDefault` | `general.newSessionDefault` | String | Default session type for new terminals |
| `reopenProjectsOnLaunch` | `general.reopenProjectsOnLaunch` | Bool | Whether to restore open projects on launch |
| `openProjectURLs` | `general.openProjectURLs` | [String] | List of project URLs to reopen |
| `maxScanWorkers` | `general.maxScanWorkers` | Int | Maximum concurrent file scan workers |

#### ai

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `enabled` | `ai.enabled` | Bool | Whether AI features are enabled |
| `provider` | `ai.provider` | String | AI service provider identifier |
| `apiKey` | `ai.apiKey` | String | API key for the AI provider |
| `model` | `ai.model` | String | AI model name/identifier |

#### profiles

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `activeProfileID` | `profiles.activeProfileID` | String (UUID) | ID of the currently active color profile |

#### settings

| Constant Name | Key String | Type | Description |
|--------------|-----------|------|-------------|
| `sidebarWidth` | `settings.sidebarWidth` | Double | Width of the settings window sidebar in points |

## Logging

Subsystem: `{{bundle_id}}` | Category: `SettingsKeys`

| Event | Level | Message |
|-------|-------|---------|
| Duplicate key detected | error | `SettingsKeys: duplicate key value "{{key}}" found` |
| Deprecated key accessed | debug | `SettingsKeys: deprecated key "{{key}}" accessed — migration pending` |
| Key migration performed | info | `SettingsKeys: migrated "{{oldKey}}" to "{{newKey}}"` |

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

## Design Decisions

_None yet — decisions made during implementation should be recorded here._

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [separation-of-concerns](agenticdevelopercookbook://compliance/best-practices#separation-of-concerns) | partial | Best Practices |
| [state-recovery](agenticdevelopercookbook://compliance/reliability#state-recovery) | partial | Reliability |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-10-04 | Mike Fullerton | Retarget centralized-keys reference to the settings-window recipe URI |
| 1.1.0 | 2026-10-04 | Mike Fullerton | Conform to the ingredient format: section order, non-standard sections folded into allowed ones, Compliance added |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

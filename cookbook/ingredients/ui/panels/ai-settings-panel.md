---
id: 24eb3821-0f66-4acf-bff0-5797982bb60d
title: "AI Settings Panel"
domain: agenticdevelopercookbook://ingredients/ui/panels/ai-settings-panel
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-05
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Settings panel for AI/LLM provider configuration with multi-provider support"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
tags:
  - ai-settings-panel
  - panel
  - ui
depends-on: []
related:
  - ingredient.ui.component.ai-chat-control
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# AI Settings Panel

## Overview

A settings panel for configuring AI/LLM provider integration. Appears as a category within the settings window (see `settings-window.md`). This spec covers both the settings UI and the provider interface pattern.

The panel follows the interface-first pattern (Rules 17-19): settings are stored locally, the actual AI provider is injected via protocol/interface. The settings panel configures which provider, model, and credentials to use. The application consumes AI capabilities exclusively through the `AIProvider` protocol — the settings panel is the configuration surface, not the integration point.

This is BOTH a settings UI spec AND an interface design for AI integration. The UI configures preferences; the interface abstracts the provider. They are decoupled by design — the panel writes configuration, and the provider factory reads it to construct the active provider.

## Terminology

| Term | Definition |
|------|-----------|
| Provider | An AI/LLM service backend (e.g., Anthropic, OpenAI, a local model server) |
| Model | A specific model offered by a provider (e.g., claude-sonnet-4-6, gpt-4o) |
| API key | A secret credential used to authenticate with a provider's API |
| Endpoint | The base URL for a provider's API |
| Connection status | The result of a test call to the configured provider: connected, disconnected, or untested |
| Secure storage | Platform-specific credential storage (Keychain, EncryptedSharedPreferences, HttpOnly cookies) — NOT UserDefaults, SharedPreferences, or localStorage |

## Behavioral Requirements

### General

- **settings-category**: The AI settings panel MUST appear as a category named "AI" within the settings window.
- **enable-toggle**: An "Enable AI Features" toggle MUST be present at the top of the panel. Default value MUST be `false` (off).
- **disable-dims-controls**: When AI features are disabled, all other controls in the panel MUST be visually disabled (dimmed/grayed) and non-interactive. The controls MUST remain visible so the user can see what configuration is available.

### Provider selection

- **provider-picker-options**: The panel MUST display a provider picker with the following options:
  - Claude (Anthropic)
  - OpenAI (ChatGPT)
  - Google (Gemini)
  - Custom (OpenAI-compatible)
- **default-provider-claude**: The default provider selection MUST be Claude (Anthropic).
- **provider-change-updates-ui**: Changing the provider MUST immediately update the model picker options and show/hide the endpoint section as appropriate.

### Authentication

- **secure-key-input**: The panel MUST display an API Key field using a secure/masked input control (`SecureField` on Apple, masked `EditText` on Android, `<input type="password">` on Web).
- **secure-key-storage**: API keys MUST be stored in platform secure storage:
  - Apple: Keychain Services
  - Android: EncryptedSharedPreferences / Android Keystore
  - Web: HttpOnly secure cookies (server-assisted) — NEVER `localStorage` or `sessionStorage`
- **no-insecure-key-storage**: API keys MUST NOT be stored in UserDefaults, SharedPreferences, localStorage, SQLite, or any unencrypted persistence layer.
- **non-sensitive-storage-tiers**: Non-sensitive AI settings (provider, model, endpoint URL, timeout, enable toggle) follow the settings window storage tier:
  - **Simple**: `UserDefaults` / `@AppStorage` (macOS/iOS), `SharedPreferences` / `DataStore` (Android), `localStorage` (Web)
  - **Complex**: SQLite or equivalent structured database — appropriate for apps that already use SQLite for other persistence, need migration-safe schema changes, or store settings alongside relational data
  - Either tier is conformant. The choice SHOULD be consistent with the app's overall settings storage strategy (see `settings-window.md` abstract-persistence).
- **no-key-in-logs**: API keys MUST NOT appear in any log output, crash reports, analytics events, or debug panel displays — even at debug level.
- **masked-key-display**: The API key field MUST NOT be pre-populated with the full key value when revisiting the panel. It SHOULD display a masked placeholder (e.g., "••••••••••••abcd" showing only the last 4 characters) if a key is stored, or be empty if no key is stored.

### Model selection

- **model-picker-options**: The panel MUST display a model picker whose options depend on the selected provider:
  - **Claude (Anthropic)**: claude-haiku-4-5-20251001, claude-sonnet-4-5-20250514, claude-opus-4-5-20250514
  - **OpenAI**: gpt-4.1-nano, gpt-4.1-mini, gpt-4o-mini, gpt-4o
  - **Google (Gemini)**: gemini-2.0-flash, gemini-2.5-flash-preview-05-20, gemini-2.5-pro-preview-05-06
  - **Custom**: (no preset models — custom model name field only)
- **dynamic-model-fetch**: The model list SHOULD be fetched dynamically from the provider's API where supported (e.g., Anthropic and OpenAI list-models endpoints), with the hardcoded defaults in model-picker-options as fallback.
- **silent-model-fetch-fallback**: When dynamic model fetching fails, the panel MUST fall back to the hardcoded defaults silently — no error dialog. A debug-level log message MUST be emitted.
- **custom-model-override**: A custom model name text field MUST be displayed below the model picker. It MUST be editable for all providers. When a value is entered, it overrides the picker selection.

### Endpoint configuration

- **endpoint-custom-only**: The endpoint section MUST be visible only when the provider is set to "Custom".
- **endpoint-fields**: The endpoint section MUST include:
  - Base URL text field (placeholder: `http://localhost:11434`)
  - Timeout stepper or picker (values: 15s, 30s, 60s, 120s, 300s; default: 30s)
- **url-validation**: The Base URL field MUST validate that the entered value is a well-formed URL. Invalid URLs MUST be indicated with an inline error message (e.g., "Invalid URL format") but MUST NOT prevent the user from typing.

### Connection status

- **connection-status-indicator**: The panel MUST display a connection status indicator:
  - **Connected**: Green dot with label "Connected"
  - **Disconnected**: Red dot with label "Disconnected"
  - **Untested**: Gray dot with label "Not tested"
- **initial-status-untested**: The initial connection status MUST be "Untested" (gray dot).
- **test-connection-button**: A "Test Connection" button MUST be present next to the connection status indicator.
- **test-connection-flow**: When the user taps "Test API Key", the panel MUST:
  1. Show an indeterminate progress indicator (spinner) inline with the button
  2. Send a minimal completion request to the configured provider (e.g., `"Hi"` with `max_tokens: 1`)
  3. Apply a timeout of 15 seconds for the test call
  4. Display the result inline: success (green checkmark + "API key is valid") or failure (red X + error message)
  5. On failure, display the provider's error message (e.g., "Authentication failed", "invalid x-api-key")
- **auto-test-debounce**: The panel SHOULD automatically trigger a connection test when the provider, API key, or endpoint changes — with a debounce of 2 seconds after the last change. Implementations MAY defer this to a manual "Test" action.
- **async-connection-test**: The connection test MUST NOT block the UI. It MUST run asynchronously.

## AI Provider Interface Pattern

### Protocol definition

The `AIProvider` protocol defines the contract for all AI provider implementations. The settings panel configures WHICH provider is active and supplies credentials. Application code consumes AI capabilities exclusively through this interface.

```
AIProvider {
  func complete(prompt: String, options: CompletionOptions) async throws -> String
  func stream(prompt: String, options: CompletionOptions) -> AsyncStream<String>
  var isConfigured: Bool { get }
  var providerName: String { get }
  var supportedModels: [String] { get async }
}

CompletionOptions {
  model: String
  maxTokens: Int?
  temperature: Double?
  systemPrompt: String?
}
```

### Implementations

- **claude-provider-impl**: A `ClaudeProvider` implementation MUST exist for the Anthropic API.
- **openai-provider-impl**: An `OpenAIProvider` implementation MUST exist for the OpenAI API.
- **google-custom-provider-impl**: A `GoogleProvider` implementation MUST exist for the Google Gemini API. A `CustomProvider` implementation MUST exist for OpenAI-compatible endpoints (e.g., Ollama, LM Studio).
- **mock-provider-impl**: A `MockProvider` implementation MUST exist for testing. It MUST return deterministic canned responses and MUST NOT make network calls.
- **runtime-provider-resolution**: The active provider MUST be resolved at runtime based on the settings panel configuration, using a factory or dependency injection container.
- **tls-required**: All providers MUST use TLS/HTTPS for network communication. The `CustomProvider` MAY allow HTTP for `localhost` addresses only.
- **no-cached-keys-in-providers**: Provider implementations MUST NOT store or cache API keys internally. They MUST retrieve credentials from secure storage on each use or accept them via injection at construction time.

## Appearance

```
┌──────────────────────────────────────────────────┐
│ AI                                               │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌─ General ──────────────────────────────────┐  │
│  │ Enable AI Features           [  toggle  ]  │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  ┌─ Provider ─────────────────────────────────┐  │
│  │ Provider          [Claude (Anthropic)  ▾]  │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  ┌─ Model ────────────────────────────────────┐  │
│  │ Model             [claude-haiku-4-5... ▾]  │  │
│  │ Custom Model      [                     ]  │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  ┌─ Authentication ───────────────────────────┐  │
│  │ ••••••••••••                      [Clear]  │  │
│  │ API Key           [Enter new key...     ]  │  │
│  │ [Test API Key]  ✅ API key is valid        │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  ┌─ Quick Chat ───────────────────────────────┐  │
│  │ (see ingredient.ui.component.ai-chat-control)            │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
└──────────────────────────────────────────────────┘
```

With Custom provider selected, the Endpoint section appears above Quick Chat:

```
│  ┌─ Endpoint ─────────────────────────────────┐  │
│  │ Base URL          [https://api.example.com] │  │
│  └────────────────────────────────────────────┘  │
```

- **Layout**: Vertical form with grouped sections, consistent with settings window content panel style
- **Controls**: Native controls only — toggle, picker, secure text field, text field, stepper, button
- **Status dot**: 8pt circle, filled — green (`#34C759` / systemGreen), red (`#FF3B30` / systemRed), gray (`#8E8E93` / systemGray)
- **Section headers**: Platform-native grouped form section headers
- **Disabled state**: All controls below the enable toggle use reduced opacity (0.4) when AI features are disabled

## States

| State | Behavior |
|-------|----------|
| AI features disabled | Enable toggle is off; all other controls are dimmed and non-interactive |
| AI features enabled, no key | Enable toggle is on; controls are interactive; connection status is "Untested" |
| AI features enabled, key entered | Controls interactive; enable toggle auto-set to on (auto-enable-on-key-entry) |
| Connection testing | Spinner on Test Connection button; status shows previous state until test completes |
| Connected | Green dot, "Connected" label |
| Disconnected | Red dot, "Disconnected" label, error description shown below |
| Provider changed | Model picker updates options; endpoint section shows/hides; connection status resets to "Untested" |
| Dynamic model fetch in progress | Model picker shows current options with a subtle loading indicator |
| Dynamic model fetch failed | Model picker shows hardcoded defaults; debug log emitted |
| Custom model entered | Custom model field value overrides picker selection |
| Invalid URL entered | Inline error below Base URL field; Test Connection button still available |

## Accessibility

- **control-a11y-labels**: All form controls MUST have accessible labels matching their visible labels (e.g., "Enable AI Features", "Provider", "API Key", "Model").
- **status-a11y-label**: The connection status indicator MUST have an accessibility label that includes both the status and any error message (e.g., "Connection status: Disconnected. Authentication failed.").
- **status-not-color-only**: The status dot MUST NOT rely solely on color to convey state. The text label ("Connected", "Disconnected", "Not tested") MUST always be displayed alongside the dot.
- **secure-field-announce**: The secure API key field MUST be announced as a secure text field by screen readers.
- **disabled-state-announce**: When controls are disabled (AI features off), screen readers MUST announce them as disabled/dimmed.
- **keyboard-tab-order**: The panel MUST be fully keyboard-navigable. Tab order MUST follow the visual layout top to bottom: Enable toggle, Provider picker, API Key field, Model picker, Custom model field, Endpoint fields (if visible), Test Connection button.
- **test-loading-announce**: The Test Connection button MUST announce its loading state to screen readers when a test is in progress (e.g., "Test Connection, testing...").

### Auto-enable behavior

- **auto-enable-on-key-entry**: When the user enters a new API key, the "Enable AI Features" toggle MUST be automatically set to `true` (on). The user MAY subsequently disable it manually.

### Quick Chat

- **inline-chat-control**: The panel MUST include an inline chat control (see `ingredient.ui.component.ai-chat-control`) at the bottom of the panel, below all configuration fields. This allows the user to verify the configuration by sending a real message.
- **chat-respects-toggle**: The chat control MUST respect the "Enable AI Features" toggle — when AI features are disabled, sending messages MUST be blocked with an inline error message.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| ai-001 | enable-toggle | Open AI settings panel for the first time | Enable AI Features toggle is off |
| ai-002 | disable-dims-controls | AI features toggle is off, attempt to interact with Provider picker | Picker is non-interactive (disabled) |
| ai-003 | disable-dims-controls | AI features toggle is off | All controls below toggle are visually dimmed |
| ai-004 | default-provider-claude | Enable AI features, observe provider picker | Claude (Anthropic) is selected by default |
| ai-005 | provider-change-updates-ui | Change provider from Claude to OpenAI | Model picker shows gpt-4o, gpt-4o-mini, o3-mini |
| ai-006 | provider-change-updates-ui | Change provider to Local | Endpoint section becomes visible |
| ai-007 | provider-change-updates-ui | Change provider from Local to Claude | Endpoint section is hidden |
| ai-008 | secure-key-storage, no-insecure-key-storage | Enter API key, inspect platform storage | Key is in Keychain/EncryptedSharedPreferences, NOT in UserDefaults/SharedPreferences/localStorage |
| ai-009 | masked-key-display | Store an API key "sk-ant-abc123xyz", close and reopen panel | Field shows "••••••••••••xyz" (masked with last 4 chars visible) |
| ai-010 | model-picker-options | Select Claude provider | Model picker shows claude-sonnet-4-6, claude-opus-4-6, claude-haiku-4-5 |
| ai-011 | model-picker-options | Select Local provider | Model picker shows local-default |
| ai-012 | custom-model-override | Enter "my-fine-tuned-model" in custom model field | Custom model value is used instead of picker selection |
| ai-013 | endpoint-custom-only | Select Claude provider | Endpoint section is not visible |
| ai-014 | endpoint-custom-only | Select Custom provider | Endpoint section is visible |
| ai-015 | url-validation | Enter "not a url" in Base URL field | Inline error "Invalid URL format" displayed |
| ai-016 | url-validation | Enter "https://api.example.com" in Base URL field | No inline error displayed |
| ai-017 | connection-status-indicator, initial-status-untested | Open panel with no prior configuration | Status shows gray dot with "Not tested" |
| ai-018 | test-connection-flow | Configure valid provider and key, tap Test Connection | Spinner shown during test; status updates to green "Connected" on success |
| ai-019 | test-connection-flow | Configure invalid API key, tap Test Connection | Status updates to red "Disconnected"; error "Authentication failed" shown |
| ai-020 | test-connection-flow | Configure provider with unreachable endpoint, tap Test Connection | Status updates to red "Disconnected"; error "Network unreachable" or "Timeout" shown |
| ai-021 | auto-test-debounce | Change API key, wait 2 seconds | Connection test triggers automatically |
| ai-022 | auto-test-debounce | Change API key three times within 1 second | Only one connection test runs (after 2s from last change) |
| ai-023 | async-connection-test | Trigger connection test | UI remains responsive; other controls are interactive during test |
| ai-024 | no-key-in-logs | Enter API key, check all log output | API key value does not appear in any log message |
| ai-025 | mock-provider-impl | Inject MockProvider, call complete() | Returns deterministic canned response without network call |
| ai-026 | tls-required | Configure Claude provider | All API calls use HTTPS |
| ai-027 | tls-required | Configure Local provider with http://localhost:11434 | HTTP is allowed for localhost |
| ai-028 | tls-required | Configure Local provider with http://remote-server.com | Connection MUST use HTTPS; HTTP rejected for non-localhost |
| ai-029 | status-not-color-only | Inspect connection status with VoiceOver | Both the dot color AND text label are present; label announced by screen reader |
| ai-030 | keyboard-tab-order | Press Tab repeatedly through the panel | Focus moves top-to-bottom through all interactive controls |
| ai-031 | dynamic-model-fetch | Configure valid Claude API key, open model picker | Model list includes dynamically fetched models from Anthropic API |
| ai-032 | silent-model-fetch-fallback | Configure Claude provider with no network | Model picker shows hardcoded defaults; debug log contains fallback message |
| ai-033 | auto-enable-on-key-entry | Enter a new API key while enable toggle is off | Enable toggle switches to on automatically |
| ai-034 | auto-enable-on-key-entry | Enter a new API key while enable toggle is already on | Enable toggle remains on (no change) |
| ai-035 | inline-chat-control | Open AI settings with valid key configured | Quick Chat section visible at bottom of panel |
| ai-036 | chat-respects-toggle | Disable AI features, type message in Quick Chat, send | Error message "AI features are disabled" displayed in chat |

## Edge Cases

- **Invalid API key**: Connection test returns "Authentication failed" (401/403). Status shows red dot. User can correct the key and retest.
- **Network unavailable**: Connection test returns "Network unreachable". Status shows red dot. Panel remains fully interactive for editing configuration.
- **Provider deprecates a model**: If the selected model is no longer in the dynamically fetched list, the panel SHOULD show a warning badge next to the model picker and log a warning. The model selection SHOULD be preserved (not silently changed) so the user can decide.
- **API key format invalid**: Some providers have known key prefixes (e.g., `sk-ant-` for Anthropic, `sk-` for OpenAI). The panel MAY validate the format and show an inline hint, but MUST NOT prevent saving a key that doesn't match the expected prefix (the format may change).
- **Endpoint returns unexpected response**: Connection test shows "Disconnected" with "Unexpected response" error. Does not crash.
- **Extremely long API key**: The secure field MUST handle keys up to 1000 characters without truncation or crash.
- **Concurrent settings changes**: If the user changes multiple settings rapidly while a connection test is in progress, the in-flight test SHOULD be cancelled and a new one scheduled (debounce).
- **Secure storage unavailable**: If Keychain/EncryptedSharedPreferences is unavailable (e.g., locked device, sandboxing issue), the panel MUST show an error message: "Unable to store credentials securely. Please check your device settings." It MUST NOT fall back to insecure storage.
- **Provider API rate-limited during model fetch**: Fall back to hardcoded defaults. Log at debug level. Do not show an error to the user.
- **Empty API key submitted for test**: Test Connection button SHOULD be disabled when the API key field is empty (except for Local provider which may not require a key).
- **Migration from insecure storage**: If an older version stored keys in UserDefaults, SQLite, localStorage, or any unencrypted layer, the implementation SHOULD migrate them to secure storage on first launch and delete the insecure copy.

## Configuration

This ingredient has no configurable options.

## Logging

Subsystem: `{{bundle_id}}` | Category: `AISettingsPanel`

| Event | Level | Message |
|-------|-------|---------|
| Panel opened | debug | `AISettingsPanel: opened` |
| Panel closed | debug | `AISettingsPanel: closed` |
| AI features toggled | debug | `AISettingsPanel: AI features {{enabled\|disabled}}` |
| Provider changed | debug | `AISettingsPanel: provider changed to "{{provider}}"` |
| Model changed | debug | `AISettingsPanel: model changed to "{{model}}"` |
| Custom model set | debug | `AISettingsPanel: custom model set to "{{model}}"` |
| API key stored | debug | `AISettingsPanel: API key stored for "{{provider}}"` |
| API key removed | debug | `AISettingsPanel: API key removed for "{{provider}}"` |
| Connection test started | debug | `AISettingsPanel: connection test started for "{{provider}}"` |
| Connection test succeeded | debug | `AISettingsPanel: connection test succeeded ({{duration}}ms)` |
| Connection test failed | debug | `AISettingsPanel: connection test failed: {{error}}` |
| Dynamic model fetch started | debug | `AISettingsPanel: fetching models from "{{provider}}"` |
| Dynamic model fetch succeeded | debug | `AISettingsPanel: fetched {{count}} models from "{{provider}}"` |
| Dynamic model fetch failed | debug | `AISettingsPanel: model fetch failed for "{{provider}}", using defaults` |
| Endpoint changed | debug | `AISettingsPanel: endpoint changed to "{{url}}"` |
| Timeout changed | debug | `AISettingsPanel: timeout changed to {{seconds}}s` |
| Secure storage error | error | `AISettingsPanel: secure storage unavailable: {{error}}` |
| Insecure key migration | info | `AISettingsPanel: migrated API key from insecure storage to secure storage for "{{provider}}"` |

**Critical logging rule**: API key values MUST NEVER appear in log output at any level. Log messages reference the provider name or key existence, never the key value.

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Connection test spinner uses a static "testing..." label instead of animation |
| Reduce Transparency | Section backgrounds use opaque fills |
| Increase Contrast | Status dots use higher-contrast colors; disabled controls use 0.3 opacity instead of 0.4 |
| Differentiate Without Color | Status indicator includes an icon alongside the dot: checkmark (connected), xmark (disconnected), minus (untested) |
| VoiceOver / TalkBack | All controls announced with labels and states; secure field announced as password field; status announced with full context |
| Bold Text | Labels respond to Dynamic Type bold setting |

## Privacy

- **Data collected**: Provider selection, model selection, endpoint URL, timeout preference, connection status. API key (credential).
- **Sensitive data**: API keys are classified as sensitive credentials.
- **Storage**:
  - API keys: Platform secure storage ONLY (Keychain, EncryptedSharedPreferences, HttpOnly cookies). See secure-key-storage, no-insecure-key-storage.
  - Non-sensitive preferences (provider, model, endpoint URL, timeout, enable toggle): Either simple tier (UserDefaults / SharedPreferences / localStorage) or complex tier (SQLite) — see non-sensitive-storage-tiers.
  - Connection status: In-memory only, not persisted.
- **Transmission**: API keys are transmitted only to the configured provider endpoint over TLS/HTTPS. They are never sent to analytics, crash reporting, or any other service.
- **Retention**: Preferences persist until the user changes them or the app is uninstalled. API keys persist in secure storage until explicitly removed by the user or app uninstall.
- **Logging**: API keys MUST NOT appear in any log output (no-key-in-logs). Provider names and connection results are logged at debug level.

## Platform Notes

- **SwiftUI (macOS / iOS / visionOS)**: Implement as a `Form` with `Section` groups inside the settings window's content panel. Use `SecureField` for the API key. Store the API key via `KeychainAccess` or direct Security framework calls (`SecItemAdd`, `SecItemCopyMatching`). Non-sensitive settings use either `@AppStorage` (simple tier) or SQLite via the app's database manager (complex tier) — see non-sensitive-storage-tiers. For the provider picker, use `Picker` with `.pickerStyle(.menu)`. Status dot: `Circle().fill(color).frame(width: 8, height: 8)`. Connection test: use `async/await` with `Task` and `withTaskCancellationHandler` for debounce. Dynamic model fetch: `URLSession` with `JSONDecoder`. Timeout: use `URLRequest.timeoutInterval`. For the enable/disable dimming, apply `.disabled(!isAIEnabled)` and `.opacity(isAIEnabled ? 1.0 : 0.4)` to the sections below the toggle.
- **Compose (Android)**: Use `Column` with `Card` sections. API key field: `OutlinedTextField` with `visualTransformation = PasswordVisualTransformation()`. Store key via `EncryptedSharedPreferences` from `androidx.security.crypto`. Non-sensitive settings in `DataStore` or `SharedPreferences`. Provider picker: `ExposedDropdownMenuBox`. Status dot: `Canvas` with `drawCircle`. Connection test: `viewModelScope.launch` with `withTimeout`. Debounce with `Flow.debounce(2000)`. Disable controls via `enabled = isAIEnabled` parameter and alpha modifier.
- **React / Web**: Use a form with `<select>` for pickers, `<input type="password">` for API key. API key storage: send to a server endpoint that stores in an HttpOnly secure cookie or server-side encrypted store — NEVER use `localStorage` or `sessionStorage` for API keys. Non-sensitive settings: `localStorage`. Status dot: `<span>` with CSS `border-radius: 50%` and background color. Connection test: `fetch` with `AbortController` for timeout and cancellation. Debounce: `setTimeout`/`clearTimeout` or a utility like `lodash.debounce`.

## Feature Flags

| Flag Key | Default | Description |
|----------|---------|-------------|
| `ai.enabled` | `false` | Master gate for all AI features across the app |
| `ai.dynamic_models` | `true` | Whether to attempt dynamic model list fetching |
| `ai.custom_provider` | `true` | Whether the Custom provider option is available |

## Design Decisions

**UI-stub implementation**: The initial implementation from scratching-post is UI-only — settings are stored via `@AppStorage` but no actual AI provider calls are wired up. The `AIProvider` protocol, concrete provider implementations (Claude, OpenAI, Local), connection testing, and dynamic model fetching are all spec-only requirements awaiting implementation. The settings UI is functional and persists values, but the values are not consumed by any AI integration code yet.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

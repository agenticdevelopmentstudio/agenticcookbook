<!-- leaf: ingredients-ui/panels-ai-settings-panel · source: ingredients/ui/panels/ai-settings-panel.md -->

**Rules** (cite as `ingredients-ui/panels-ai-settings-panel#<slug>`):

- `settings-category` MUST
- `enable-toggle` MUST
- `disable-dims-controls` MUST
- `provider-picker-options` MUST
- `default-provider-claude` MUST
- `provider-change-updates-ui` MUST
- `secure-key-input` MUST
- `secure-key-storage` MUST
- `no-insecure-key-storage` MUST
- `non-sensitive-storage-tiers` SHOULD
- `no-key-in-logs` MUST
- `masked-key-display` MUST
- `model-picker-options` MUST
- `dynamic-model-fetch` SHOULD
- `silent-model-fetch-fallback` MUST
- `custom-model-override` MUST
- `endpoint-custom-only` MUST
- `endpoint-fields` MUST
- `url-validation` MUST
- `connection-status-indicator` MUST
- `initial-status-untested` MUST
- `test-connection-button` MUST
- `test-connection-flow` MUST
- `auto-test-debounce` SHOULD
- `async-connection-test` MUST
- `claude-provider-impl` MUST
- `openai-provider-impl` MUST
- `google-custom-provider-impl` MUST
- `mock-provider-impl` MUST
- `runtime-provider-resolution` MUST
- `tls-required` MUST
- `no-cached-keys-in-providers` MUST

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


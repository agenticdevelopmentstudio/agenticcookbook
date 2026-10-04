
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


<!-- leaf: ingredients-ui/panels-ai-settings-panel--part-2 · source: ingredients/ui/panels/ai-settings-panel.md -->

# AI Settings Panel — continued (part 2)

**Rules** (cite as `ingredients-ui/panels-ai-settings-panel--part-2#<slug>`):

- `control-a11y-labels` MUST
- `status-a11y-label` MUST
- `status-not-color-only` MUST
- `secure-field-announce` MUST
- `disabled-state-announce` MUST
- `keyboard-tab-order` MUST
- `test-loading-announce` MUST
- `auto-enable-on-key-entry` MUST
- `inline-chat-control` MUST
- `chat-respects-toggle` MUST
- `logging` MUST — API keys MUST NOT appear in any log output (no-key-in-logs). Provider names and connection results are logged at debug …

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

## Configuration

This ingredient has no configurable options.

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

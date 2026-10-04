
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


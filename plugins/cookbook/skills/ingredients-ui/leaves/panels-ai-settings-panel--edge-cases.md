<!-- leaf: ingredients-ui/panels-ai-settings-panel--edge-cases · source: ingredients/ui/panels/ai-settings-panel.md -->

# AI Settings Panel

**Rules** (cite as `ingredients-ui/panels-ai-settings-panel--edge-cases#<slug>`):

- `provider-deprecates-a-model` SHOULD — If the selected model is no longer in the dynamically fetched list, the panel SHOULD show a warning badge next to the …
- `api-key-format-invalid` MUST — Some providers have known key prefixes (e.g., sk-ant- for Anthropic, sk- for OpenAI). The panel MAY validate the format …
- `extremely-long-api-key` MUST — The secure field MUST handle keys up to 1000 characters without truncation or crash.
- `concurrent-settings-changes` SHOULD — If the user changes multiple settings rapidly while a connection test is in progress, the in-flight test SHOULD be …
- `secure-storage-unavailable` MUST — If Keychain/EncryptedSharedPreferences is unavailable (e.g., locked device, sandboxing issue), the panel MUST show an …
- `empty-api-key-submitted-for-test` SHOULD — Test Connection button SHOULD be disabled when the API key field is empty (except for Local provider which may not …
- `migration-from-insecure-storage` SHOULD — If an older version stored keys in UserDefaults, SQLite, localStorage, or any unencrypted layer, the implementation …

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

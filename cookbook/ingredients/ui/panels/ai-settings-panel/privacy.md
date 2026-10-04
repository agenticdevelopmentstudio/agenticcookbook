
- **Data collected**: Provider selection, model selection, endpoint URL, timeout preference, connection status. API key (credential).
- **Sensitive data**: API keys are classified as sensitive credentials.
- **Storage**:
  - API keys: Platform secure storage ONLY (Keychain, EncryptedSharedPreferences, HttpOnly cookies). See secure-key-storage, no-insecure-key-storage.
  - Non-sensitive preferences (provider, model, endpoint URL, timeout, enable toggle): Either simple tier (UserDefaults / SharedPreferences / localStorage) or complex tier (SQLite) — see non-sensitive-storage-tiers.
  - Connection status: In-memory only, not persisted.
- **Transmission**: API keys are transmitted only to the configured provider endpoint over TLS/HTTPS. They are never sent to analytics, crash reporting, or any other service.
- **Retention**: Preferences persist until the user changes them or the app is uninstalled. API keys persist in secure storage until explicitly removed by the user or app uninstall.
- **Logging**: API keys MUST NOT appear in any log output (no-key-in-logs). Provider names and connection results are logged at debug level.


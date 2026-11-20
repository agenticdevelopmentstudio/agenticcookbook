
- `must-use-platform-secure-storage`: whether every token, credential and sensitive value uses platform secure storage
- `must-not-store-secrets-in-plaintext`: whether any secret sits in plaintext configuration, app settings or an unencrypted preference store
- `should-use-keychain-on-apple`: whether Apple code uses Keychain Services for sensitive data
- `must-not-store-secrets-in-userdefaults-or-plists`: whether any secret is stored in UserDefaults or plists
- `should-use-encrypted-storage-on-android`: whether Android code uses `EncryptedSharedPreferences` or the Android Keystore for sensitive data
- `must-not-store-secrets-in-plain-sharedpreferences`: whether any secret is stored in plain SharedPreferences
- `should-use-dpapi-for-windows-local-secrets`: whether Windows-only local secrets use DPAPI with `CurrentUser` scope
- `should-use-user-secrets-for-development-only`: whether User Secrets are used for development-time secrets only
- `must-not-store-tokens-in-plaintext-config`: whether any C# token or credential is in plaintext config or app settings

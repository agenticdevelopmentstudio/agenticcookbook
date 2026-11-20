
- `must-use-platform-secure-storage`: every token, credential and sensitive value is stored in platform secure storage
- `must-not-store-secrets-in-plaintext`: no secret is in plaintext configuration, app settings or an unencrypted preference store
- `should-use-keychain-on-apple`: Apple sensitive data is in Keychain Services, or the code says why not
- `must-not-store-secrets-in-userdefaults-or-plists`: no secret is in UserDefaults or a plist
- `should-use-encrypted-storage-on-android`: Android sensitive data is in `EncryptedSharedPreferences` or the Android Keystore, or the code says why not
- `must-not-store-secrets-in-plain-sharedpreferences`: no secret is in plain SharedPreferences
- `should-use-dpapi-for-windows-local-secrets`: Windows-only local secrets use DPAPI with `DataProtectionScope.CurrentUser`, or the code says why not
- `should-use-user-secrets-for-development-only`: development secrets use User Secrets and production does not, or the code says why not
- `must-not-store-tokens-in-plaintext-config`: no C# token or credential is in plaintext config files or app settings

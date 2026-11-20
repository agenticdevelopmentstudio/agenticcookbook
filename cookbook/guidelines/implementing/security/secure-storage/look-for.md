
- `must-use-platform-secure-storage`: a token, credential or other sensitive value stored anywhere but the platform's secure storage breaks it
- `must-not-store-secrets-in-plaintext`: a secret in a plaintext configuration file, app settings or an unencrypted preference store breaks it
- `should-use-keychain-on-apple`: sensitive data on Apple platforms stored outside Keychain Services
- `must-not-store-secrets-in-userdefaults-or-plists`: a secret written to `UserDefaults` or a plist breaks it
- `should-use-encrypted-storage-on-android`: sensitive data on Android stored outside `EncryptedSharedPreferences` or the Android Keystore
- `must-not-store-secrets-in-plain-sharedpreferences`: a secret written to plain `SharedPreferences` breaks it
- `should-use-dpapi-for-windows-local-secrets`: a Windows-only local secret not protected with `ProtectedData.Protect` under `DataProtectionScope.CurrentUser`
- `should-use-user-secrets-for-development-only`: development secrets kept outside User Secrets, or User Secrets relied on in production
- `must-not-store-tokens-in-plaintext-config`: a token or credential in a plaintext config file or app settings (`appsettings.json`) breaks it

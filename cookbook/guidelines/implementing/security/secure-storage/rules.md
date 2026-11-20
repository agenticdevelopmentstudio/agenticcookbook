
- **must-use-platform-secure-storage**: Tokens, credentials, and any sensitive data MUST use platform secure storage.
- **must-not-store-secrets-in-plaintext**: You **MUST NOT** store secrets in plaintext configuration files, app settings, or unencrypted preference stores.
- **should-use-keychain-on-apple**: On Apple platforms, you **SHOULD** use Keychain Services for tokens, credentials, and any sensitive data.
- **must-not-store-secrets-in-userdefaults-or-plists**: On Apple platforms, you **MUST NOT** store secrets in UserDefaults or plists.
- **should-use-encrypted-storage-on-android**: On Android, you **SHOULD** use `EncryptedSharedPreferences` or the Android Keystore for tokens, credentials, and sensitive data.
- **must-not-store-secrets-in-plain-sharedpreferences**: On Android, you **MUST NOT** store secrets in plain SharedPreferences.
- **should-use-dpapi-for-windows-local-secrets**: In C#, you **SHOULD** use [DPAPI](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.protecteddata) (`ProtectedData.Protect`/`Unprotect` with `DataProtectionScope.CurrentUser`) for Windows-only local secrets.
- **should-use-user-secrets-for-development-only**: In C#, you **SHOULD** use [User Secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets) (`Microsoft.Extensions.Configuration.UserSecrets`) for development-time secrets only (plaintext JSON — not for production).
- **must-not-store-tokens-in-plaintext-config**: In C#, you **MUST NOT** store tokens or credentials in plaintext config files or app settings.

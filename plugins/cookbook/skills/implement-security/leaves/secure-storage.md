<!-- leaf: implement-security/secure-storage · source: guidelines/implementing/security/secure-storage.md -->

**Rules** (cite as `implement-security/secure-storage#<slug>`):

- `credentials-sensitive-data-use-platform-secure-storage` MUST — Tokens, credentials, and any sensitive data MUST use platform secure storage. Never store secrets in plaintext …

# Secure Storage

Tokens, credentials, and any sensitive data MUST use platform secure storage. Never store secrets in plaintext configuration files, app settings, or unencrypted preference stores.

## Swift

Use Keychain Services for tokens, credentials, and any sensitive data. Never store secrets in UserDefaults or plists.

## Kotlin

Use `EncryptedSharedPreferences` or the Android Keystore for tokens, credentials, and sensitive data. Never store secrets in plain SharedPreferences.

## C#

- Use [DPAPI](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.protecteddata) (`ProtectedData.Protect`/`Unprotect` with `DataProtectionScope.CurrentUser`) for Windows-only local secrets
- Use [User Secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets) (`Microsoft.Extensions.Configuration.UserSecrets`) for development-time secrets only (plaintext JSON — not for production)
- Never store tokens or credentials in plaintext config files or app settings

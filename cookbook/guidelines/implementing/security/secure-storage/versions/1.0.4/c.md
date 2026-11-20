
- Use [DPAPI](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.protecteddata) (`ProtectedData.Protect`/`Unprotect` with `DataProtectionScope.CurrentUser`) for Windows-only local secrets
- Use [User Secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets) (`Microsoft.Extensions.Configuration.UserSecrets`) for development-time secrets only (plaintext JSON — not for production)
- Never store tokens or credentials in plaintext config files or app settings


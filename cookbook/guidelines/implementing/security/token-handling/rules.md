
### Access tokens

- **should-keep-access-tokens-short-lived**: Access tokens **SHOULD** be short-lived (5-15 min).
- **should-include-only-necessary-claims**: You **SHOULD** include only necessary claims — no PII in JWTs that transit untrusted parties.

### Refresh tokens

- **should-bind-refresh-tokens-to-client**: Refresh tokens are longer-lived but **SHOULD** be bound to the client.
- **should-rotate-refresh-tokens**: You **SHOULD** use rotation for refresh tokens (see Authentication above).
- **should-store-refresh-tokens-server-side**: You **SHOULD** store refresh tokens server-side when possible.

### Token refresh strategy

- **should-refresh-proactively**: You **SHOULD** refresh proactively before expiry (e.g., at 75% of TTL).
- **should-queue-requests-during-refresh**: You **SHOULD** queue concurrent requests during refresh to avoid race conditions.
- **should-retry-refresh-with-backoff**: You **SHOULD** retry with backoff on refresh failure.

### Secure storage per platform

- **should-use-keychain-on-apple**: On Apple platforms, you **SHOULD** store tokens in Keychain Services.
- **should-use-encrypted-storage-on-android**: On Android, you **SHOULD** store tokens in EncryptedSharedPreferences / Android Keystore.
- **should-use-dpapi-on-windows**: On Windows, you **SHOULD** store tokens with DPAPI (`ProtectedData`).
- **should-use-httponly-cookies-on-web**: On the web, you **SHOULD** store tokens in HttpOnly Secure SameSite cookies (never localStorage).

### Never do these

- **must-not-store-tokens-in-web-storage**: Tokens **MUST NOT** be stored in `localStorage` or `sessionStorage` (XSS-accessible).
- **must-not-put-tokens-in-query-parameters**: Tokens **MUST NOT** be put in URL query parameters (logged in server logs, browser history, referrer headers).
- **must-validate-jwt-alg-against-allowlist**: `alg: none` **MUST NOT** be used in JWTs — the `alg` header **MUST** be validated server-side against an allowlist.
- **must-not-trust-client-jwt-claims**: Client-supplied JWT claims **MUST NOT** be trusted for authorization without server-side verification.

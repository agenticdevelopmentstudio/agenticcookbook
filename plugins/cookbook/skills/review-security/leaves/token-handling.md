<!-- leaf: review-security/token-handling · source: guidelines/reviewing/security/token-handling.md -->

**Rules** (cite as `review-security/token-handling#<slug>`):

- `tokens-not-stored-localstorage-sessionstorage-xss` MUST — Tokens MUST NOT be stored in localStorage or sessionStorage (XSS-accessible)
- `tokens-not-put-url-query-parameters` MUST — Tokens MUST NOT be put in URL query parameters (logged in server logs, browser history, referrer headers)
- `alg-none-not-used-jwts-alg-header` MUST — alg: none MUST NOT be used in JWTs — the alg header MUST be validated server-side against an allowlist
- `supplied-jwt-claims-not-trusted-authorization-without-server` MUST — Client-supplied JWT claims MUST NOT be trusted for authorization without server-side verification

# Token Handling

Keep access tokens short-lived (5-15 min), store refresh tokens in secure platform storage, and rotate them on every use.

### Access tokens

Short-lived (5-15 min). Include only necessary claims — no PII in JWTs
that transit untrusted parties.

### Refresh tokens

Longer-lived but bound to client. Use rotation (see Authentication above).
Store server-side when possible.

### Token refresh strategy

- Proactive refresh before expiry (e.g., at 75% of TTL)
- Queue concurrent requests during refresh to avoid race conditions
- Retry with backoff on refresh failure

### Secure storage per platform

See also agenticdevelopercookbook://guidelines/reviewing/security/privacy

- **Apple:** Keychain Services
- **Android:** EncryptedSharedPreferences / Android Keystore
- **Windows:** DPAPI (`ProtectedData`)
- **Web:** HttpOnly Secure SameSite cookies (never localStorage)

### Never do these

- Tokens MUST NOT be stored in `localStorage` or `sessionStorage` (XSS-accessible)
- Tokens MUST NOT be put in URL query parameters (logged in server logs, browser history, referrer headers)
- `alg: none` MUST NOT be used in JWTs — the `alg` header MUST be validated server-side against an allowlist
- Client-supplied JWT claims MUST NOT be trusted for authorization without server-side verification

References:
- [RFC 6750: Bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750)
- [RFC 7519: JSON Web Tokens](https://datatracker.ietf.org/doc/html/rfc7519)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)

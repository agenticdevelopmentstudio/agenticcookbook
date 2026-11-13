
# Authentication

Use OAuth 2.0 / OpenID Connect with PKCE for all public clients. The Implicit flow is
deprecated — OAuth 2.1 removes it entirely.

**Per-platform auth flow:**
- **Native apps (iOS/Android/Windows):** Authorization Code + PKCE via the system browser
  (`ASWebAuthenticationSession`, Custom Tabs, `WebAuthenticationBroker`). Apps MUST NOT embed a
  WebView for auth — the app can intercept credentials.
- **SPAs:** Authorization Code + PKCE. Consider a Backend-for-Frontend (BFF) pattern where
  the SPA never handles tokens directly — the BFF holds tokens server-side in HttpOnly cookies.
- **Server-to-server:** Client Credentials flow.

**Session management:**
- Short-lived access tokens (5-15 minutes)
- Refresh token rotation MUST be used — each use issues a new refresh token and invalidates the old one.
  Detect reuse of a revoked refresh token and invalidate the entire token family.
- Absolute session timeouts server-side

References:
- [RFC 7636: PKCE](https://datatracker.ietf.org/doc/html/rfc7636)
- [RFC 8252: OAuth for Native Apps](https://datatracker.ietf.org/doc/html/rfc8252)
- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html)


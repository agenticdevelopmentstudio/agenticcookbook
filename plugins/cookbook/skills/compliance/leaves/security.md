<!-- leaf: compliance/security · source: compliance/security.md -->

**Rules** (cite as `compliance/security#<slug>`):

- `authentication-use-oauth-oidc-pkce` MUST — Authentication MUST use OAuth 2.0/OIDC with PKCE for all public clients.
- `authorization-enforced-server-side-never` MUST — Authorization MUST be enforced server-side, never client-only.
- `secrets-credentials-use-platform-specific-secure` MUST — Secrets and credentials MUST use platform-specific secure storage (Keychain, EncryptedSharedPreferences, DPAPI).
- `user-input-validated-sanitized-before-processing` MUST — All user input MUST be validated and sanitized before processing.
- `network-communication-use-tls-higher` MUST — All network communication MUST use TLS 1.2 or higher.
- `log-messages-not-contain-credentials-tokens-pii` MUST — Log messages MUST NOT contain credentials, tokens, or PII.
- `access-tokens-short-lived-15-min` MUST — Access tokens MUST be short-lived (5-15 min) with refresh token rotation.
- `dependencies-scanned-known-vulnerabilities-before` MUST — Dependencies MUST be scanned for known vulnerabilities before release.
- `web-responses-include-standard-security-headers` MUST — Web responses MUST include standard security headers (HSTS, CSP, X-Content-Type-Options).
- `web-content-enforce-strict-content-security` MUST — Web content MUST enforce a strict Content Security Policy.
- `cors-use-explicit-origin-allowlists` MUST — CORS MUST use explicit origin allowlists, never wildcards with credentials.
- `verification-include-static-analysis-sast` MUST — Verification MUST include static analysis (SAST) and dependency scanning.

# Security Compliance

Security compliance covers the foundational safeguards every recipe and guideline must observe — authentication, authorization, transport encryption, input handling, secret management, and dependency hygiene. These checks ensure that implementations meet baseline security expectations across all platforms.

## Applicability

This category applies to any recipe or guideline that handles user credentials, secrets, network communication, user input, dependencies, or web content delivery. If a recipe touches authentication, stores sensitive data, accepts external input, or serves content over HTTP, it falls within scope.

## Checks

### secure-authentication

Authentication MUST use OAuth 2.0/OIDC with PKCE for all public clients.

**Applies when:** recipe implements or integrates an authentication flow.

**Guidelines:**
- Authentication

---

### server-side-authorization

Authorization MUST be enforced server-side, never client-only.

**Applies when:** recipe includes authorization logic or role-based access control.

**Guidelines:**
- Authorization

---

### secure-storage

Secrets and credentials MUST use platform-specific secure storage (Keychain, EncryptedSharedPreferences, DPAPI).

**Applies when:** recipe stores tokens, passwords, API keys, or other sensitive material.

**Guidelines:**
- Secure Storage

---

### input-sanitization

All user input MUST be validated and sanitized before processing.

**Applies when:** recipe accepts user input in any form (text fields, file uploads, query parameters, deep links).

**Guidelines:**
- Input Validation

---

### secure-transport

All network communication MUST use TLS 1.2 or higher.

**Applies when:** recipe makes or receives network requests.

**Guidelines:**
- Transport Security

---

### secure-log-output

Log messages MUST NOT contain credentials, tokens, or PII.

**Applies when:** recipe produces log output or diagnostic messages.

**Guidelines:**
- Sensitive Data
- Logging

---

### token-lifecycle

Access tokens MUST be short-lived (5-15 min) with refresh token rotation.

**Applies when:** recipe issues, stores, or refreshes access tokens.

**Guidelines:**
- Token Handling

---

### dependency-scanning

Dependencies MUST be scanned for known vulnerabilities before release.

**Applies when:** recipe introduces or relies on third-party dependencies.

**Guidelines:**
- Dependency Security

---

### security-headers

Web responses MUST include standard security headers (HSTS, CSP, X-Content-Type-Options).

**Applies when:** recipe serves web content or defines HTTP responses.

**Guidelines:**
- Security Headers Checklist

---

### content-security-policy

Web content MUST enforce a strict Content Security Policy.

**Applies when:** recipe renders HTML or loads external resources in a web context.

**Guidelines:**
- Content Security Policy

---

### cors-allowlist

CORS MUST use explicit origin allowlists, never wildcards with credentials.

**Applies when:** recipe configures cross-origin resource sharing.

**Guidelines:**
- CORS

---

### security-testing

Verification MUST include static analysis (SAST) and dependency scanning.

**Applies when:** recipe defines a verification or CI pipeline.

**Guidelines:**
- Security Testing

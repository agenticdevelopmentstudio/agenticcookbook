---
id: 5CECB56F-B15C-42F0-BEB2-58861B33EC8B
title: "Security Compliance"
domain: agenticdevelopercookbook://compliance/security
type: compliance
version: 1.0.1
status: draft
language: en
created: 2026-03-28
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compliance checks for authentication, authorization, transport security, and secure coding practices."
platforms: []
tags: [compliance, security]
depends-on: []
related:
  - agenticdevelopercookbook://compliance/privacy-and-data
  - agenticdevelopercookbook://compliance/user-safety
  - agenticdevelopercookbook://compliance/reliability
references: []
---

# Security Compliance

Security compliance covers the foundational safeguards every recipe and guideline must observe — authentication, authorization, transport encryption, input handling, secret management, and dependency hygiene. These checks ensure that implementations meet baseline security expectations across all platforms.

## Applicability

This category applies to any recipe or guideline that handles user credentials, secrets, network communication, user input, dependencies, or web content delivery. If a recipe touches authentication, stores sensitive data, accepts external input, or serves content over HTTP, it falls within scope.

## Checks

### secure-authentication

Authentication MUST use OAuth 2.0/OIDC with PKCE for all public clients.

**Applies when:** recipe implements or integrates an authentication flow.

**Guidelines:**
- [Authentication](agenticdevelopercookbook://guidelines/implementing/security/authentication)

---

### server-side-authorization

Authorization MUST be enforced server-side, never client-only.

**Applies when:** recipe includes authorization logic or role-based access control.

**Guidelines:**
- [Authorization](agenticdevelopercookbook://guidelines/implementing/security/authorization)

---

### secure-storage

Secrets and credentials MUST use platform-specific secure storage (Keychain, EncryptedSharedPreferences, DPAPI).

**Applies when:** recipe stores tokens, passwords, API keys, or other sensitive material.

**Guidelines:**
- [Secure Storage](agenticdevelopercookbook://guidelines/implementing/security/secure-storage)

---

### input-sanitization

All user input MUST be validated and sanitized before processing.

**Applies when:** recipe accepts user input in any form (text fields, file uploads, query parameters, deep links).

**Guidelines:**
- [Input Validation](agenticdevelopercookbook://guidelines/implementing/security/input-validation)

---

### secure-transport

All network communication MUST use TLS 1.2 or higher.

**Applies when:** recipe makes or receives network requests.

**Guidelines:**
- [Transport Security](agenticdevelopercookbook://guidelines/implementing/security/transport-security)

---

### secure-log-output

Log messages MUST NOT contain credentials, tokens, or PII.

**Applies when:** recipe produces log output or diagnostic messages.

**Guidelines:**
- [Sensitive Data](agenticdevelopercookbook://guidelines/implementing/security/sensitive-data)
- [Logging](agenticdevelopercookbook://guidelines/implementing/observability/logging)

---

### token-lifecycle

Access tokens MUST be short-lived (5-15 min) with refresh token rotation.

**Applies when:** recipe issues, stores, or refreshes access tokens.

**Guidelines:**
- [Token Handling](agenticdevelopercookbook://guidelines/implementing/security/token-handling)

---

### dependency-scanning

Dependencies MUST be scanned for known vulnerabilities before release.

**Applies when:** recipe introduces or relies on third-party dependencies.

**Guidelines:**
- [Dependency Security](agenticdevelopercookbook://guidelines/implementing/security/dependency-security)

---

### security-headers

Web responses MUST include standard security headers (HSTS, CSP, X-Content-Type-Options).

**Applies when:** recipe serves web content or defines HTTP responses.

**Guidelines:**
- [Security Headers Checklist](agenticdevelopercookbook://guidelines/implementing/security/security-headers-checklist)

---

### content-security-policy

Web content MUST enforce a strict Content Security Policy.

**Applies when:** recipe renders HTML or loads external resources in a web context.

**Guidelines:**
- [Content Security Policy](agenticdevelopercookbook://guidelines/implementing/security/content-security-policy)

---

### cors-allowlist

CORS MUST use explicit origin allowlists, never wildcards with credentials.

**Applies when:** recipe configures cross-origin resource sharing.

**Guidelines:**
- [CORS](agenticdevelopercookbook://guidelines/implementing/security/cors)

---

### security-testing

Verification MUST include static analysis (SAST) and dependency scanning.

**Applies when:** recipe defines a verification or CI pipeline.

**Guidelines:**
- [Security Testing](agenticdevelopercookbook://guidelines/testing/security-testing)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |

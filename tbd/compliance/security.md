---
id: 5CECB56F-B15C-42F0-BEB2-58861B33EC8B
title: "Security Compliance"
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
  - tbd/compliance/privacy-and-data.md
  - tbd/compliance/user-safety.md
  - tbd/compliance/reliability.md
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
- [adc.guideline.implementing.security.authentication](cookbook:aec38334-67fa-4c7e-bca2-607932af3f22)

---

### server-side-authorization

Authorization MUST be enforced server-side, never client-only.

**Applies when:** recipe includes authorization logic or role-based access control.

**Guidelines:**
- [adc.guideline.implementing.security.authorization](cookbook:2609037a-fb89-4b49-88b0-7e4295e5d6f6)

---

### secure-storage

Secrets and credentials MUST use platform-specific secure storage (Keychain, EncryptedSharedPreferences, DPAPI).

**Applies when:** recipe stores tokens, passwords, API keys, or other sensitive material.

**Guidelines:**
- [adc.guideline.implementing.security.secure-storage](cookbook:926dff1a-dc12-46a4-b8c1-bdedbc142afd)

---

### input-sanitization

All user input MUST be validated and sanitized before processing.

**Applies when:** recipe accepts user input in any form (text fields, file uploads, query parameters, deep links).

**Guidelines:**
- [adc.guideline.implementing.security.input-validation](cookbook:4ca8a3d5-cdcc-4f74-a2ec-3a198608b419)

---

### secure-transport

All network communication MUST use TLS 1.2 or higher.

**Applies when:** recipe makes or receives network requests.

**Guidelines:**
- [adc.guideline.implementing.security.transport-security](cookbook:5b026378-d418-406a-9aab-6e3f043901af)

---

### secure-log-output

Log messages MUST NOT contain credentials, tokens, or PII.

**Applies when:** recipe produces log output or diagnostic messages.

**Guidelines:**
- [adc.guideline.implementing.security.sensitive-data](cookbook:22f1ca04-2d1d-4faf-8bf0-c6abcd60802c)
- [adc.guideline.implementing.observability.logging](cookbook:0f0c1da3-1c53-417b-890d-0259d7513c65)

---

### token-lifecycle

Access tokens MUST be short-lived (5-15 min) with refresh token rotation.

**Applies when:** recipe issues, stores, or refreshes access tokens.

**Guidelines:**
- [adc.guideline.implementing.security.token-handling](cookbook:2598f495-1820-47e7-b7e7-ce548d390148)

---

### dependency-scanning

Dependencies MUST be scanned for known vulnerabilities before release.

**Applies when:** recipe introduces or relies on third-party dependencies.

**Guidelines:**
- [adc.guideline.implementing.security.dependency-security](cookbook:b712c766-af1f-4716-b8fb-34bf0bbb13eb)

---

### security-headers

Web responses MUST include standard security headers (HSTS, CSP, X-Content-Type-Options).

**Applies when:** recipe serves web content or defines HTTP responses.

**Guidelines:**
- [adc.guideline.implementing.security.security-headers-checklist](cookbook:12d6b9fe-d1a0-4b9f-b772-41d9b4aa0b8a)

---

### content-security-policy

Web content MUST enforce a strict Content Security Policy.

**Applies when:** recipe renders HTML or loads external resources in a web context.

**Guidelines:**
- [adc.guideline.implementing.security.content-security-policy](cookbook:6f4cfd55-cb09-4ede-a53c-feaeb5781127)

---

### cors-allowlist

CORS MUST use explicit origin allowlists, never wildcards with credentials.

**Applies when:** recipe configures cross-origin resource sharing.

**Guidelines:**
- [adc.guideline.implementing.security.cors](cookbook:8ea0409f-405a-4f4d-9bbf-54bf21c86d33)

---

### security-testing

Verification MUST include static analysis (SAST) and dependency scanning.

**Applies when:** recipe defines a verification or CI pipeline.

**Guidelines:**
- [adc.guideline.testing.security-testing](cookbook:cf05e36f-ea8b-4af2-8df6-c5e772dc25b5)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |

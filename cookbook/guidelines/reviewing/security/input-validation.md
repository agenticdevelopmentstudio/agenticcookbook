---
id: d02a65e0-652f-49b9-be3b-44fccc2f7888
title: "Input Validation"
domain: agenticdevelopercookbook://guidelines/reviewing/security/input-validation
type: guideline
version: 1.1.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "**Never trust client input.** Client-side validation is a UX feature, not a security control."
platforms:
  - typescript
  - web
tags:
  - input-validation
  - security
depends-on: []
related: []
references:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - input-handling
  - security-review
  - api-integration
---

# Input Validation

Validate all input server-side using allowlists, parameterized queries, and context-specific output encoding. Client-side validation is UX, not security.

**Never trust client input.** Client-side validation is a UX feature, not a security control.
All validation must be duplicated server-side.

- **Allowlists over denylists** — validation SHOULD define what is valid, not what is invalid. Denylists have gaps.
- **Validate, sanitize, escape** — in that order. Validation rejects. Sanitization cleans.
  Escaping is context-specific output encoding (HTML, URL, SQL, JS).
- **Parameterized queries** MUST be used — the only reliable defense against SQL injection. User input MUST NOT be concatenated
  into queries.
- **Output encoding** — context-dependent: HTML-encode for HTML, URL-encode for URLs. Use
  framework auto-escaping (React JSX, Django templates) and understand when it does NOT apply
  (e.g., raw HTML insertion APIs — always sanitize with a library like DOMPurify first).
- **File uploads** — MIME type MUST be validated server-side (not just extension). Limit size. Store
  outside web root. Files MUST NOT be served with original filename or from the same origin.

## Server-render and Server-Action boundary

Server-side rendering and server-invoked functions create a deserialization boundary where
client-controlled input is reconstructed and executed in a trusted context.

- **Validate at the boundary** — untrusted input crossing a server-side deserialization boundary
  (e.g., RSC Server Action arguments, the RSC Flight payload, or any equivalent serialized
  request body) MUST be schema-validated and type-checked before use. The framework's
  serialization layer is not a validation layer.
- **No secrets in server-rendered components** — server-rendered output MUST NOT embed secrets,
  credentials, or internal-only data, since the rendered payload is sent to the client.
- **Rate-limit server-render endpoints** — render and server-action endpoints SHOULD be
  rate-limited to bound the cost of crafted or repeated requests.
- **Pin to a patched framework version** — the rendering framework MUST be pinned to a version
  that includes current security patches for its serialization boundary.

References:
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-06-09 | Mike Fullerton | Extend validation to the server-render / server-action boundary |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

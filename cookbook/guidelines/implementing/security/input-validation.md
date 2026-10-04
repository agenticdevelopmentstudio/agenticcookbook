---
id: 4ca8a3d5-cdcc-4f74-a2ec-3a198608b419
title: "Input Validation"
domain: agenticdevelopercookbook://guidelines/implementing/security/input-validation
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-06-10
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
  - https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
  - https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/
  - https://arxiv.org/html/2508.14925v1
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
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

The trust boundary extends to server-side deserialization. Untrusted input that crosses a
server-side deserialization boundary — RSC Server Action arguments, the React Server Components
Flight payload, or the equivalent boundary in any server-render framework — MUST be
schema-validated (e.g., with Zod) before use; the boundary is a deserialization sink, not a typed
contract. Secrets MUST NOT be embedded in components that render on the server. Server-render
endpoints SHOULD be rate-limited. The framework SHOULD be pinned to a patched version.

References:
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.1.0 | 2026-06-09 | Mike Fullerton | Extend validation to the server-render / server-action boundary |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

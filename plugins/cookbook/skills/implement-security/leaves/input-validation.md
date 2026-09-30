<!-- leaf: implement-security/input-validation · source: guidelines/implementing/security/input-validation.md -->

**Rules** (cite as `implement-security/input-validation#<slug>`):

- `allowlists-over-denylists` SHOULD — validation SHOULD define what is valid, not what is invalid. Denylists have gaps.
- `parameterized-queries` MUST — MUST be used — the only reliable defense against SQL injection. User input MUST NOT be concatenated into queries.
- `file-uploads` MUST — MIME type MUST be validated server-side (not just extension). Limit size. Store outside web root. Files MUST NOT be …
- `server-render-framework-schema-validated-zod-before` MUST — The trust boundary extends to server-side deserialization. Untrusted input that crosses a server-side deserialization …

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

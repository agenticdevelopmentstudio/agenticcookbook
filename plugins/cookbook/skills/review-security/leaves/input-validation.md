<!-- leaf: review-security/input-validation · source: guidelines/reviewing/security/input-validation.md -->

**Rules** (cite as `review-security/input-validation#<slug>`):

- `allowlists-over-denylists` SHOULD — validation SHOULD define what is valid, not what is invalid. Denylists have gaps.
- `parameterized-queries` MUST — MUST be used — the only reliable defense against SQL injection. User input MUST NOT be concatenated into queries.
- `file-uploads` MUST — MIME type MUST be validated server-side (not just extension). Limit size. Store outside web root. Files MUST NOT be …
- `validate-at-the-boundary` MUST — untrusted input crossing a server-side deserialization boundary (e.g., RSC Server Action arguments, the RSC Flight …
- `no-secrets-in-server-rendered-components` MUST — server-rendered output MUST NOT embed secrets, credentials, or internal-only data, since the rendered payload is sent …
- `rate-limit-server-render-endpoints` SHOULD — render and server-action endpoints SHOULD be rate-limited to bound the cost of crafted or repeated requests.
- `pin-to-a-patched-framework-version` MUST — the rendering framework MUST be pinned to a version that includes current security patches for its serialization …

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

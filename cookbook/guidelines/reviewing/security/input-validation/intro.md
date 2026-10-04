
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


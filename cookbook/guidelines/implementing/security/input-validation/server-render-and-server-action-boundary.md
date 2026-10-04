
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


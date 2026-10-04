
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


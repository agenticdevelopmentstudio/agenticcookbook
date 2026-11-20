
- **must-not-trust-client-input**: Client input **MUST NOT** be trusted.
- **must-duplicate-validation-server-side**: All validation **MUST** be duplicated server-side.
- **should-prefer-allowlists-over-denylists**: Validation SHOULD define what is valid, not what is invalid (allowlists over denylists).
- **should-validate-sanitize-escape-in-order**: Input **SHOULD** be validated, sanitized, then escaped — in that order.
  - Validation rejects. Sanitization cleans.
    Escaping is context-specific output encoding (HTML, URL, SQL, JS).
- **must-use-parameterized-queries**: Parameterized queries MUST be used — the only reliable defense against SQL injection.
- **must-not-concatenate-input-into-queries**: User input MUST NOT be concatenated into queries.
- **should-encode-output-per-context**: Output encoding **SHOULD** be context-dependent: HTML-encode for HTML, URL-encode for URLs.
- **should-use-framework-auto-escaping**: You **SHOULD** use framework auto-escaping (React JSX, Django templates) and understand when it does NOT apply (e.g., raw HTML insertion APIs).
- **must-sanitize-before-raw-html-insertion**: Input to raw HTML insertion APIs **MUST** always be sanitized with a library like DOMPurify first.
- **must-validate-upload-mime-server-side**: For file uploads, MIME type MUST be validated server-side (not just extension).
- **should-limit-upload-size**: File upload size **SHOULD** be limited.
- **should-store-uploads-outside-web-root**: Uploaded files **SHOULD** be stored outside web root.
- **must-not-serve-uploads-as-uploaded**: Files MUST NOT be served with original filename or from the same origin.
- **must-validate-at-deserialization-boundary**: Untrusted input crossing a server-side deserialization boundary (e.g., RSC Server Action arguments, the RSC Flight payload, or any equivalent serialized request body) MUST be schema-validated and type-checked before use.
- **must-not-embed-secrets-in-server-rendered-output**: Server-rendered output MUST NOT embed secrets, credentials, or internal-only data, since the rendered payload is sent to the client.
- **should-rate-limit-server-render-endpoints**: Render and server-action endpoints SHOULD be rate-limited to bound the cost of crafted or repeated requests.
- **must-pin-patched-framework-version**: The rendering framework MUST be pinned to a version that includes current security patches for its serialization boundary.

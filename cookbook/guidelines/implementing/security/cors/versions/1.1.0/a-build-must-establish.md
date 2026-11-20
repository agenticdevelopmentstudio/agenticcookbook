
- `should-not-enable-cors-unless-configured-correctly`: CORS is enabled only on endpoints that need cross-origin access, each configured per these rules, or the code says why
- `must-not-reflect-origin`: `Access-Control-Allow-Origin` is never set from the request's Origin header without an allowlist match
- `should-maintain-explicit-origin-allowlist`: allowed origins are an explicit list, or the code says why not
- `must-not-use-wildcard-with-credentials`: no response pairs `Access-Control-Allow-Origin: *` with credentials
- `should-cache-preflight`: preflight responses set `Access-Control-Max-Age: 86400`, or the code says why not
- `should-minimize-exposed-headers`: every exposed header is one the client uses, or the code says why
- `should-not-match-origins-with-unanchored-regex`: every origin pattern is anchored, or the code says why not
- `should-not-allow-null-origin`: `null` is not an allowed origin, or the code says why
- `should-not-allow-broad-methods-and-headers`: allowed methods and headers are only those the API uses, or the code says why


- **should-not-enable-cors-unless-configured-correctly**: CORS **SHOULD** be configured correctly or not enabled at all.
- **must-not-reflect-origin**: The Origin header MUST NOT be reflected back as `Access-Control-Allow-Origin`.
- **should-maintain-explicit-origin-allowlist**: An explicit allowlist of origins **SHOULD** be maintained.
- **must-not-use-wildcard-with-credentials**: `*` MUST NOT be used with credentials — browsers block this, and attempting it reveals a design misunderstanding.
- **should-cache-preflight**: SHOULD set `Access-Control-Max-Age: 86400` to reduce preflight overhead.
- **should-minimize-exposed-headers**: Exposed headers **SHOULD** be minimized: only what the client actually needs.
- **should-not-match-origins-with-unanchored-regex**: Origins **SHOULD NOT** be matched by regex without anchoring (`evil-example.com` matching `example.com`).
- **should-not-allow-null-origin**: The `null` origin **SHOULD NOT** be allowed (exploitable via sandboxed iframes).
- **should-not-allow-broad-methods-and-headers**: Allowed methods and headers **SHOULD NOT** be overly broad.


- `should-not-enable-cors-unless-configured-correctly`: whether CORS is enabled only where it is configured correctly
- `must-not-reflect-origin`: whether the Origin header is ever reflected back as `Access-Control-Allow-Origin`
- `should-maintain-explicit-origin-allowlist`: whether allowed origins come from an explicit allowlist
- `must-not-use-wildcard-with-credentials`: whether `*` is ever used with credentials
- `should-cache-preflight`: whether preflight responses set `Access-Control-Max-Age: 86400`
- `should-minimize-exposed-headers`: whether exposed headers are only what the client actually needs
- `should-not-match-origins-with-unanchored-regex`: whether any origin regex is unanchored
- `should-not-allow-null-origin`: whether the `null` origin is allowed
- `should-not-allow-broad-methods-and-headers`: whether allowed methods and headers are overly broad

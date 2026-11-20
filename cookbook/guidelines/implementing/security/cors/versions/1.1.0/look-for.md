
- `should-not-enable-cors-unless-configured-correctly`: CORS enabled with a configuration that is not deliberately right, where it could be left off
- `must-not-reflect-origin`: code that copies the request's `Origin` into `Access-Control-Allow-Origin` breaks it
- `should-maintain-explicit-origin-allowlist`: origins allowed by anything other than an explicit allowlist
- `must-not-use-wildcard-with-credentials`: `Access-Control-Allow-Origin: *` together with credentials breaks it
- `should-cache-preflight`: no `Access-Control-Max-Age` (86400) on preflight responses
- `should-minimize-exposed-headers`: `Access-Control-Expose-Headers` listing headers the client does not need
- `should-not-match-origins-with-unanchored-regex`: an origin regex with no anchors, so `evil-example.com` matches `example.com`
- `should-not-allow-null-origin`: `null` accepted as an allowed origin
- `should-not-allow-broad-methods-and-headers`: allowed methods or headers set to `*` or far wider than the API uses

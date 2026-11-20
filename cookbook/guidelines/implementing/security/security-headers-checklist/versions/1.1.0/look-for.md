
- `must-set-hsts`: a response with no `Strict-Transport-Security` header, or one missing `max-age=31536000`, `includeSubDomains` or `preload`, breaks it
- `must-set-csp`: a response with no `Content-Security-Policy`, or one without `default-src 'none'` and a nonce-based `script-src` with `'strict-dynamic'`, breaks it
- `must-set-nosniff`: a response without `X-Content-Type-Options: nosniff` breaks it
- `must-set-frame-options-deny`: a response without `X-Frame-Options: DENY` breaks it
- `must-set-referrer-policy`: a response without `Referrer-Policy: strict-origin-when-cross-origin` breaks it
- `must-set-permissions-policy`: a response without a `Permissions-Policy` that disables camera, microphone and geolocation breaks it
- `must-set-no-store-on-sensitive-responses`: a sensitive response without `Cache-Control: no-store` breaks it

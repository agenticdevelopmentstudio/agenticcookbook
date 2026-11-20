
- `must-set-hsts`: every response carries `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
- `must-set-csp`: every response carries a `Content-Security-Policy` with `default-src 'none'` and `script-src 'nonce-{random}' 'strict-dynamic'`
- `must-set-nosniff`: every response carries `X-Content-Type-Options: nosniff`
- `must-set-frame-options-deny`: every response carries `X-Frame-Options: DENY`
- `must-set-referrer-policy`: every response carries `Referrer-Policy: strict-origin-when-cross-origin`
- `must-set-permissions-policy`: every response carries `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- `must-set-no-store-on-sensitive-responses`: every sensitive response carries `Cache-Control: no-store`

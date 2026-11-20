
- `must-set-hsts`: whether every response sets `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
- `must-set-csp`: whether every response sets the `Content-Security-Policy` with `default-src 'none'` and a nonce-based, `'strict-dynamic'` `script-src`
- `must-set-nosniff`: whether every response sets `X-Content-Type-Options: nosniff`
- `must-set-frame-options-deny`: whether every response sets `X-Frame-Options: DENY`
- `must-set-referrer-policy`: whether every response sets `Referrer-Policy: strict-origin-when-cross-origin`
- `must-set-permissions-policy`: whether every response sets `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- `must-set-no-store-on-sensitive-responses`: whether every sensitive response sets `Cache-Control: no-store`

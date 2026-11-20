
- **must-set-hsts**: Every web application **MUST** set `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`.
- **must-set-csp**: Every web application **MUST** set `Content-Security-Policy: default-src 'none'; script-src 'nonce-{random}' 'strict-dynamic'; ...`.
- **must-set-nosniff**: Every web application **MUST** set `X-Content-Type-Options: nosniff`.
- **must-set-frame-options-deny**: Every web application **MUST** set `X-Frame-Options: DENY`.
- **must-set-referrer-policy**: Every web application **MUST** set `Referrer-Policy: strict-origin-when-cross-origin`.
- **must-set-permissions-policy**: Every web application **MUST** set `Permissions-Policy: camera=(), microphone=(), geolocation=()`.
- **must-set-no-store-on-sensitive-responses**: Every web application **MUST** set `Cache-Control: no-store` for sensitive responses.

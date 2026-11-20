
# Security Headers Checklist

Every web application MUST set these response headers:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'none'; script-src 'nonce-{random}' 'strict-dynamic'; ...
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
Cache-Control: no-store  (for sensitive responses)
```


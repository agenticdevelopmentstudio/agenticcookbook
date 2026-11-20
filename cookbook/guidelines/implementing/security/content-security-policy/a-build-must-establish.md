
- `should-start-strict-from-default-src-none`: the policy sets `default-src 'none'` and each added source is one the app needs, or the code says why not
- `should-use-nonce-based-scripts`: `script-src` uses `'nonce-{random}' 'strict-dynamic'` with a fresh random nonce per response, or the code says why not
- `must-not-allow-unsafe-inline-or-eval`: `script-src` contains neither `'unsafe-inline'` nor `'unsafe-eval'`
- `should-set-frame-ancestors-self`: the policy sets `frame-ancestors 'self'`, or the code says why not
- `should-deploy-report-only-first`: every new policy shipped as `Content-Security-Policy-Report-Only` before enforcing, or the code says why not
- `should-require-trusted-types`: the CSP carries `require-trusted-types-for 'script'` and a named `trusted-types` policy, or the code says why not
- `should-back-trusted-types-with-sanitizer`: the trusted-types policy calls DOMPurify or the Sanitizer API, or the code says why not
- `should-roll-out-trusted-types-report-only-first`: Trusted Types shipped in report-only mode before enforcing, or the code says why not
- `should-enable-trusted-types-despite-mixed-support`: Trusted Types is enabled, or the code says why not

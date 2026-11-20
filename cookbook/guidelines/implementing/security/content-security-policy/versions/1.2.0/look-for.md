
- `should-start-strict-from-default-src-none`: a policy that starts from a permissive `default-src` (or none) instead of `default-src 'none'` plus only what is needed
- `should-use-nonce-based-scripts`: a `script-src` built from domain allowlists rather than `'nonce-{random}' 'strict-dynamic'`, or a nonce that is not random per response
- `must-not-allow-unsafe-inline-or-eval`: `'unsafe-inline'` or `'unsafe-eval'` in `script-src` breaks it
- `should-set-frame-ancestors-self`: a policy with no `frame-ancestors 'self'`, relying on X-Frame-Options or nothing against clickjacking
- `should-deploy-report-only-first`: a new policy enforced without first running as `Content-Security-Policy-Report-Only`
- `should-require-trusted-types`: no `require-trusted-types-for 'script'` with a named `trusted-types` policy while code assigns raw strings to `innerHTML`, `document.write` or `eval`-equivalents
- `should-back-trusted-types-with-sanitizer`: a trusted-types policy that escapes by hand instead of calling DOMPurify or the Sanitizer API (`Element.setHTML()`)
- `should-roll-out-trusted-types-report-only-first`: Trusted Types enforced without a report-only phase to surface violating sinks
- `should-enable-trusted-types-despite-mixed-support`: Trusted Types left off because not every browser supports it

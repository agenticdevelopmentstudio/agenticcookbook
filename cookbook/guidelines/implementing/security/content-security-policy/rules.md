
- **should-start-strict-from-default-src-none**: A policy **SHOULD** start strict: `default-src 'none'` then add only what is needed.
- **should-use-nonce-based-scripts**: `script-src 'nonce-{random}' 'strict-dynamic'` SHOULD be used — more secure than domain allowlisting (bypassable via JSONP/CDN scripts).
- **must-not-allow-unsafe-inline-or-eval**: Policies MUST NOT include `'unsafe-inline'` or `'unsafe-eval'` for script-src.
- **should-set-frame-ancestors-self**: A policy **SHOULD** set `frame-ancestors 'self'` to prevent clickjacking (replaces X-Frame-Options).
- **should-deploy-report-only-first**: New policies SHOULD be deployed in report-only mode first (`Content-Security-Policy-Report-Only`) to find violations before enforcing.
- **should-require-trusted-types**: The CSP **SHOULD** add `require-trusted-types-for 'script'` together with a named `trusted-types` policy so only policy-vetted typed values can be assigned to dangerous DOM sinks; raw strings are rejected.
- **should-back-trusted-types-with-sanitizer**: The trusted-types policy **SHOULD** be backed by a documented sanitizer — DOMPurify, or the Sanitizer API (`Element.setHTML()`) — rather than ad-hoc escaping.
- **should-roll-out-trusted-types-report-only-first**: Trusted Types **SHOULD** be rolled out in report-only mode first to surface violating sinks before enforcing.
- **should-enable-trusted-types-despite-mixed-support**: Trusted Types is supported in Chromium and now Safari, degrades safely (no-op) where unsupported, and has an official polyfill, so it **SHOULD** be enabled as defense-in-depth even with mixed browser support.

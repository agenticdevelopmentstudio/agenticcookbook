<!-- leaf: implement-security/content-security-policy · source: guidelines/implementing/security/content-security-policy.md -->

**Rules** (cite as `implement-security/content-security-policy#<slug>`):

- `nonce-based-scripts` SHOULD — script-src 'nonce-{random}' 'strict-dynamic' SHOULD be used — more secure than domain allowlisting (bypassable via …
- `policies-not-include-unsafe-inline-unsafe` MUST — Policies MUST NOT include 'unsafe-inline' or 'unsafe-eval' for script-src
- `new-policies-deployed-report-only-mode` SHOULD — New policies SHOULD be deployed in report-only mode first (Content-Security-Policy-Report-Only) to find violations …
- `csp-add-require-trusted-types` SHOULD — The CSP SHOULD add require-trusted-types-for 'script' together with a named trusted-types policy so only policy-vetted …
- `trusted-types-policy-backed-documented-sanitizer-dompurify` SHOULD — The trusted-types policy SHOULD be backed by a documented sanitizer — DOMPurify, or the Sanitizer API …
- `trusted-types-rolled-out-report-only` SHOULD — Trusted Types SHOULD be rolled out in report-only mode first to surface violating sinks before enforcing.
- `official-polyfill-so-enabled-defense-depth-even` SHOULD — Trusted Types is supported in Chromium and now Safari, degrades safely (no-op) where unsupported, and has an official …

# Content Security Policy

Prevent XSS and injection with a strict CSP. Web apps only.

- **Start strict:** `default-src 'none'` then add only what is needed
- **Nonce-based scripts:** `script-src 'nonce-{random}' 'strict-dynamic'` SHOULD be used — more secure than
  domain allowlisting (bypassable via JSONP/CDN scripts)
- Policies MUST NOT include `'unsafe-inline'` or `'unsafe-eval'` for script-src
- **`frame-ancestors 'self'`** to prevent clickjacking (replaces X-Frame-Options)
- New policies SHOULD be deployed in report-only mode first (`Content-Security-Policy-Report-Only`) to find
  violations before enforcing

## Trusted Types and DOM-XSS

A strict nonce-based CSP does NOT stop DOM-based XSS that flows through injection sinks like `innerHTML`,
`document.write`, or `eval`-equivalents. Harden those sinks separately:

- The CSP **SHOULD** add `require-trusted-types-for 'script'` together with a named `trusted-types` policy so
  only policy-vetted typed values can be assigned to dangerous DOM sinks; raw strings are rejected.
- The trusted-types policy **SHOULD** be backed by a documented sanitizer — DOMPurify, or the Sanitizer API
  (`Element.setHTML()`) — rather than ad-hoc escaping.
- Trusted Types **SHOULD** be rolled out in report-only mode first to surface violating sinks before enforcing.
- Trusted Types is supported in Chromium and now Safari, degrades safely (no-op) where unsupported, and has an
  official polyfill, so it **SHOULD** be enabled as defense-in-depth even with mixed browser support.

References:
- [MDN: CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [OWASP CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [Google CSP Evaluator](https://csp-evaluator.withgoogle.com/)

<!-- leaf: review-security/content-security-policy · source: guidelines/reviewing/security/content-security-policy.md -->

**Rules** (cite as `review-security/content-security-policy#<slug>`):

- `nonce-based-scripts` SHOULD — script-src 'nonce-{random}' 'strict-dynamic' SHOULD be used — more secure than domain allowlisting (bypassable via …
- `policies-not-include-unsafe-inline-unsafe` MUST — Policies MUST NOT include 'unsafe-inline' or 'unsafe-eval' for script-src
- `new-policies-deployed-report-only-mode` SHOULD — New policies SHOULD be deployed in report-only mode first (Content-Security-Policy-Report-Only) to find violations …
- `strict-csp-paired-trusted-types-lock` SHOULD — A strict CSP SHOULD be paired with Trusted Types to lock DOM injection sinks: send require-trusted-types-for 'script' …
- `trusted-types-policy-back-conversions-documented-vetted` SHOULD — The trusted-types policy SHOULD back its conversions with a documented, vetted sanitizer (e.g., DOMPurify, or the …
- `trusted-types-rolled-out-report-only` SHOULD — Trusted Types SHOULD be rolled out in report-only mode first to surface sink violations before enforcement.
- `polyfill-so-adoption-not-blocked-universal-native-support` SHOULD — Trusted Types is supported in Chromium and Safari (and forecast to expand), degrades safely where unsupported, and …

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

A strict nonce-based CSP does NOT stop DOM-XSS that flows through injection sinks like `innerHTML`, `document.write`, or `eval`-style `setTimeout` arguments — these execute without inline-script gating.

- A strict CSP SHOULD be paired with Trusted Types to lock DOM injection sinks: send `require-trusted-types-for 'script'` and declare a named policy via `trusted-types <policy-name>`.
- The trusted-types policy SHOULD back its conversions with a documented, vetted sanitizer (e.g., DOMPurify, or the Sanitizer API `setHTML`) rather than hand-rolled escaping.
- Trusted Types SHOULD be rolled out in report-only mode first to surface sink violations before enforcement.
- Trusted Types is supported in Chromium and Safari (and forecast to expand), degrades safely where unsupported, and offers a polyfill — so adoption SHOULD NOT be blocked on universal native support.

References:
- [MDN: CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [OWASP CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [Google CSP Evaluator](https://csp-evaluator.withgoogle.com/)


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


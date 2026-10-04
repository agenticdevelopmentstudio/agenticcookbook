
A strict nonce-based CSP does NOT stop DOM-XSS that flows through injection sinks like `innerHTML`, `document.write`, or `eval`-style `setTimeout` arguments — these execute without inline-script gating.

- A strict CSP SHOULD be paired with Trusted Types to lock DOM injection sinks: send `require-trusted-types-for 'script'` and declare a named policy via `trusted-types <policy-name>`.
- The trusted-types policy SHOULD back its conversions with a documented, vetted sanitizer (e.g., DOMPurify, or the Sanitizer API `setHTML`) rather than hand-rolled escaping.
- Trusted Types SHOULD be rolled out in report-only mode first to surface sink violations before enforcement.
- Trusted Types is supported in Chromium and Safari (and forecast to expand), degrades safely where unsupported, and offers a polyfill — so adoption SHOULD NOT be blocked on universal native support.

References:
- [MDN: CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [OWASP CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [Google CSP Evaluator](https://csp-evaluator.withgoogle.com/)


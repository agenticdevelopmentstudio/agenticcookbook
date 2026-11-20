
- `should-require-trusted-types`, `should-back-trusted-types-with-sanitizer`, `should-roll-out-trusted-types-report-only-first`, `should-enable-trusted-types-despite-mixed-support`: A strict nonce-based CSP does NOT stop DOM-based XSS that flows through injection sinks like `innerHTML`, `document.write`, or `eval`-equivalents, so those sinks are hardened separately.

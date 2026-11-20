
- Color-pair tokens (foreground on background) **SHOULD** be checked for WCAG 2.2 contrast (4.5:1 body text, 3:1 large text/UI) in the token pipeline, failing the build on violation.
- The token file **SHOULD** be schema-validated in CI so malformed or dangling aliases fail fast rather than shipping.


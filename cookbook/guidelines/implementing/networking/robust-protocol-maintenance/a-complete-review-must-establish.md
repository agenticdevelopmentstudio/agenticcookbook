
- `should-parse-strictly-and-reject-clearly`: whether inputs are parsed strictly against a dated, pinned spec or schema and violations rejected clearly
- `must-not-fix-up-malformed-messages`: whether any machine-to-machine path fixes up or guesses intent for malformed messages
- `should-emit-actionable-rejections`: whether rejections say what failed, which rule and the expected shape
- `should-carry-an-explicit-version`: whether the protocol or API carries an explicit version and the validated revision is pinned
- `may-soften-rejection-where-errors-amplify`: whether a softened rejection on a stateless or unauthenticated endpoint is limited to where verbose errors enable amplification or DoS, and logged internally
- `should-track-tolerated-deviations`: whether each tolerated deviation is filed, decided and closed
- `should-match-posture-to-boundary`: whether each boundary takes the posture the table gives it

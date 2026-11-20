
- `should-parse-strictly-and-reject-clearly`: inputs are parsed against a dated, pinned spec or schema version and violations are rejected, not coerced, or the code says why not
- `must-not-fix-up-malformed-messages`: no machine-to-machine path silently fixes up or guesses intent for a malformed message
- `should-emit-actionable-rejections`: each rejection names what failed, which rule and the expected shape, or the code says why not
- `should-carry-an-explicit-version`: messages carry an explicit version and the validator pins the revision it checks, or the code says why not
- `may-soften-rejection-where-errors-amplify`: where a stateless or unauthenticated endpoint softens rejection, the full detail is logged internally
- `should-track-tolerated-deviations`: each tolerated deviation has a tracked item that decides whether the spec or the sender is wrong, or the code says why not
- `should-match-posture-to-boundary`: machine-to-machine paths parse strictly and reject + report, third-party input parses strictly and degrades gracefully, and the human edge normalizes then validates, or the code says why not

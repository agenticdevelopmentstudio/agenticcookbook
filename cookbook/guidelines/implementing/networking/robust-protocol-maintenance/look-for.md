
- `should-parse-strictly-and-reject-clearly`: a parser that coerces, defaults or skips what violates the spec, or one validating against an unpinned or undated spec version.
- `must-not-fix-up-malformed-messages`: machine-to-machine code that repairs, guesses at or silently accepts a malformed protocol or API message.
- `should-emit-actionable-rejections`: a rejection that says only "bad request", without what failed, which rule and the expected shape.
- `should-carry-an-explicit-version`: a protocol or API with no explicit version, or a validator not pinned to a revision.
- `may-soften-rejection-where-errors-amplify`: verbose errors from a stateless or unauthenticated endpoint that enable amplification or DoS, or a softened rejection with no internal log.
- `should-track-tolerated-deviations`: a tolerated deviation with no tracked item, or one left as permanent behavior.
- `should-match-posture-to-boundary`: strict rejection of human input that could be normalized, or forgiving parsing on a machine-to-machine path, or third-party input with no graceful degradation.

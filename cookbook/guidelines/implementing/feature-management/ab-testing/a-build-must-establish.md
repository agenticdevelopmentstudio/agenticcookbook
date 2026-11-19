
- `experiment-provider-interface`: every experiment is evaluated through an `ExperimentProvider` by key, with the default supplied at the call site, or the code (or experiment record) says why not
- `local-default-with-debug-override`: every experiment has a local default; that default is control, its off and abort state, or the code (or experiment record) says why not; an app's debug panel has the A/B test variant picker that lets testers force a variant; the debug panel's override is unreachable in release builds; and any other override reachable in production is authenticated or signed, documented as added attack surface, and present only where needed, or the code (or experiment record) says why not
- `deterministic-hash-assignment`: a user gets the same variant on every visit, and assignment is independent across experiments; assignment is a deterministic hash of user ID and experiment ID partitioned among the variants, or the code (or experiment record) says why not
- `stable-assignment-when-allocation-changes`: raising allocation either keeps assigned users where they are or is preceded by sticky assignment; and any other change of allocation, seed or targeting that reshuffles users is preceded by sticky assignment
- `evaluation-never-fails-returns-default`: no evaluation path throws, and every error returns the caller's default
- `log-exposure-at-point-of-use`: exposure is logged where the variant is first seen, and the analysis counts only exposed users, or the code (or experiment record) says why not
- `pre-register-metric-and-sample-size`: the hypothesis, metrics and minimum sample size are recorded before the experiment starts, or the code (or experiment record) says why not
- `no-peeking`: nothing stops or extends the experiment on interim significance unless the design is sequential or Bayesian, or the code (or experiment record) says why not
- `check-sample-ratio-mismatch`: the analysis tests the observed split against the configured split (for example with a chi-square test), or the code (or experiment record) says why not; and no result is reported while a sample ratio mismatch is unexplained
- `validate-with-aa-tests`: the experimentation system has been validated with A/A tests, or the code (or experiment record) says why not
- `ramp-up-with-auto-abort`: treatments ramp up from a small percentage in steps, shut down automatically on significant harm, and the starting percentage, steps and shutdown significance level are recorded, or the code (or experiment record) says why not
- `guard-data-quality`: the analysis filters bots and measures telemetry loss per variant, and surprising results are investigated before action, or the code (or experiment record) says why not
- `watch-novelty-effects`: the analysis segments the effect by day, or the code (or experiment record) says why not
- `avoid-web-flicker`: client-side web variants apply before first paint, or the code (or experiment record) says why not
- `web-tests-follow-search-guidance`: web tests do not cloak; alternate URLs use 302 and `rel=canonical`, and test code is removed when done, or the code (or experiment record) says why not
- `app-variants-ship-in-reviewed-binary`: iOS variants use no downloaded code that introduces or changes features, are neither hidden from App Review nor undocumented, and are described with specificity in the Notes for Review and accessible for review; they ship in the reviewed binary selected by configuration, or the code (or experiment record) says why not
- `store-page-tests-use-store-tools`: store-page tests use Apple product page optimization or Google Play store listing experiments, or the code (or experiment record) says why not


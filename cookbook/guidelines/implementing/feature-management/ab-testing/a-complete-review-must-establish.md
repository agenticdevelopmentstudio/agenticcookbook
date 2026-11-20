
- Every experiment is evaluated through the provider interface by key, with a call-site default, or a recorded reason says why not
- No evaluation path can throw; every error path returns the default
- Every experiment has a local default; it is control, also its kill-switch state, or a recorded reason says why not
- An app's debug panel has the A/B test variant picker that lets testers force a variant; the debug panel's override is unreachable in release builds; and any other override reachable in production is authenticated or signed, documented as added attack surface, and present only where needed, or a recorded reason says why not
- A user keeps the same variant across visits and assignment is independent across experiments; assignment is a deterministic hash of user ID and experiment ID, or a recorded reason says why not
- Raising allocation either keeps assigned users where they are or is preceded by sticky assignment; no other allocation, seed or targeting change in a running experiment reshuffles users without sticky assignment first
- Exposure is logged where the variant is first seen, and only exposed users are analysed, or a recorded reason says why not
- Each experiment's hypothesis, metric and minimum sample size were recorded before it started, or a recorded reason says why not
- Nothing stops or extends an experiment on interim significance outside a sequential or Bayesian design, or a recorded reason says why not
- No result is reported while a sample ratio mismatch is unexplained; the analysis checks the sample ratio, filters bots, measures telemetry loss per variant and segments by day, or a recorded reason says why not
- Surprising results are investigated as possible bugs before they are acted on, or a recorded reason says why not
- The experimentation system has been validated with A/A tests, or a recorded reason says why not
- Treatments ramp up from a small percentage in recorded steps, with automatic shutdown at a recorded significance level, or a recorded reason says why not
- Web tests do not cloak; they do not flicker, use 302 and `rel=canonical` for alternate URLs, and are removed when done, or a recorded reason says why not
- iOS variants use no downloaded code that introduces or changes features, are neither hidden from App Review nor undocumented, and are described with specificity in the Notes for Review and accessible for review; they ship in the reviewed binary, or a recorded reason says why not
- Store-page tests use Apple product page optimization or Google Play store listing experiments, or a recorded reason says why not
- Every rule is kept, or the change says why not: `experiment-provider-interface`, `local-default-with-debug-override`, `deterministic-hash-assignment`, `stable-assignment-when-allocation-changes`, `evaluation-never-fails-returns-default`, `log-exposure-at-point-of-use`, `pre-register-metric-and-sample-size`, `no-peeking`, `check-sample-ratio-mismatch`, `validate-with-aa-tests`, `ramp-up-with-auto-abort`, `guard-data-quality`, `watch-novelty-effects`, `avoid-web-flicker`, `web-tests-follow-search-guidance`, `app-variants-ship-in-reviewed-binary`, `store-page-tests-use-store-tools`


A review passes when it establishes every item above.

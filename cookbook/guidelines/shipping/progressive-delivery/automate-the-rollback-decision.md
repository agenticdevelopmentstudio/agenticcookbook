
- Each step MUST define quantitative health gates *before* rollout — e.g. error rate, latency percentiles (p95/p99), and a key business metric — compared against the baseline cohort.
- Rollback SHOULD be triggered automatically when an SLO health gate fails or the error budget burns faster than the allowed rate, not by waiting for a human to notice (`fail-fast`).
- The control plane MUST expose a single kill switch that reverts exposure to the last-known-good state in one action.
- Rollback and re-application MUST be idempotent: repeating the revert produces the same safe state with no duplicate side effects (`idempotency`).
- Humans handle exceptions and ambiguous signals; routine scoring and revert SHOULD be automated.


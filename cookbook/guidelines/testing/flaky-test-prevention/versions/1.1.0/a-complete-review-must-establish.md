
- `should-quarantine-flaky-tests-immediately`: every known flaky test has been quarantined, fixed or deleted, or the code says why not
- `must-not-ignore-flaky-tests`: no flaky test is ignored
- `must-not-share-mutable-state`: no test shares mutable state with another; each arranges its own
- `must-not-depend-on-execution-order`: no test depends on execution order
- `must-not-make-real-network-calls-in-unit-tests`: no unit test makes a real network call
- `must-not-use-sleep-or-timing-assertions`: no test uses `sleep()` or a timing-dependent assertion
- `must-not-produce-filesystem-side-effects-in-unit-tests`: no unit test leaves a filesystem side effect
- `should-not-rely-on-system-clock`: no test relies on the system clock rather than injected time, or the code says why
- `must-treat-intermittent-failure-as-p1`: every intermittently failing test is tracked as a P1 bug


- **should-quarantine-flaky-tests-immediately**: Flaky tests SHOULD be quarantined immediately, then fixed or deleted.
- **must-not-ignore-flaky-tests**: A flaky test MUST NOT be ignored (never ignore).
- **must-not-share-mutable-state**: Tests MUST NOT share mutable state (each test arranges its own)
- **must-not-depend-on-execution-order**: Tests MUST NOT depend on execution order
- **must-not-make-real-network-calls-in-unit-tests**: Unit tests MUST NOT make real network calls (use fakes or stubs)
- **must-not-use-sleep-or-timing-assertions**: Tests MUST NOT use `sleep()` or timing-dependent assertions — use deterministic waits or callbacks
- **must-not-produce-filesystem-side-effects-in-unit-tests**: Unit tests MUST NOT produce filesystem side effects (use temp directories, clean up in teardown)
- **should-not-rely-on-system-clock**: Tests SHOULD NOT rely on system clock — inject time as a dependency
- **must-treat-intermittent-failure-as-p1**: If a test fails intermittently, it is broken. It MUST be treated as a P1 bug.

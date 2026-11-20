
- `should-quarantine-flaky-tests-immediately`: no test known to be flaky remains in the gating suite, or a note says why
- `must-not-ignore-flaky-tests`: each known flaky test is quarantined, fixed or deleted
- `must-not-share-mutable-state`: the suite passes with tests run in isolation and with shared mutable state absent
- `must-not-depend-on-execution-order`: the suite passes when run in a random or reversed order
- `must-not-make-real-network-calls-in-unit-tests`: the unit tests pass with network access disabled
- `must-not-use-sleep-or-timing-assertions`: the tests contain no `sleep()` call and no timing-dependent assertion
- `must-not-produce-filesystem-side-effects-in-unit-tests`: running the unit tests leaves no file outside temp directories
- `should-not-rely-on-system-clock`: time-dependent code under test takes time as an injected dependency, or a note says why not
- `must-treat-intermittent-failure-as-p1`: each intermittently failing test has an open P1 bug

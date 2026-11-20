
- `should-quarantine-flaky-tests-immediately`: known flaky tests still in the gating suite with no quarantine, fix or deletion
- `must-not-ignore-flaky-tests`: flaky tests left in place and rerun or skipped with nothing done about them
- `must-not-share-mutable-state`: module-level, class-level or global state that one test sets and another reads
- `must-not-depend-on-execution-order`: tests that pass only when another test runs first
- `must-not-make-real-network-calls-in-unit-tests`: unit tests that open real sockets or call real hosts instead of fakes or stubs
- `must-not-use-sleep-or-timing-assertions`: `sleep()` calls or assertions on elapsed time in tests
- `must-not-produce-filesystem-side-effects-in-unit-tests`: unit tests that write outside a temp directory or leave files after teardown
- `should-not-rely-on-system-clock`: tests that read the system clock instead of an injected time source
- `must-treat-intermittent-failure-as-p1`: an intermittently failing test with no P1 bug filed for it

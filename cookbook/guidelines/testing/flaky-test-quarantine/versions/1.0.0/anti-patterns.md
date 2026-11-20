
- Quarantine MUST NOT become a permanent parking lot — an unbounded, unowned quarantine list is a failure of this lifecycle.
- Deleting a flaky test to make CI green, without addressing whether the behavior still needs coverage, is silent loss of coverage and MUST NOT be done.
- Globally enabling auto-retry across the whole suite to bury flakiness MUST NOT be used as a substitute for this lifecycle.


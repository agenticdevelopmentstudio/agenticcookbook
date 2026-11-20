
- Flakiness SHOULD be detected from an objective signal: a **flip rate** (pass/fail transitions on unchanged code) above an agreed threshold, or a test that passes only on retry.
- A test that needs a retry to pass MUST be treated as flaky, even when the retry hides the failure from the gate.
- Retries MAY be used as a detection signal but MUST NOT be used as a silent cure — a test that "passes on retry 3 of 3" is a flaky test, not a passing one.
- The CI system SHOULD record per-test pass/fail history so flip rate is measurable rather than anecdotal.


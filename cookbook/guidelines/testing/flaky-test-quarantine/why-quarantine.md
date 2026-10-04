
A flaky test that blocks the gating suite trains the team to ignore red builds and rerun blindly, eroding trust in the whole suite. Quarantine removes the test from the merge gate WITHOUT deleting or silencing it — it still runs and is still tracked, so the flakiness stays visible and accountable.


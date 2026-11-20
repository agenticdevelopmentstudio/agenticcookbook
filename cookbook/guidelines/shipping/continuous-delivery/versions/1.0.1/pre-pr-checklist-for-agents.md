
1. Confirm CI runs the full automated pipeline on this branch and is green before marking the PR ready.
2. Confirm the change does not require a manual step to become releasable.
3. Confirm risky behavior is gated behind a flag so merge does not force a release.
4. Confirm a rollback or roll-forward path exists for the change.


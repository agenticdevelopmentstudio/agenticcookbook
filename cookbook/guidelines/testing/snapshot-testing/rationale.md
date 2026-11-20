
- `should-review-snapshot-files-like-source`: A diff nobody reads asserts nothing.
- `should-prefer-small-inline-snapshots`: Inline snapshots keep the expected value next to the test, so reviewers see intent in the diff.
- `should-not-snapshot-unreasonable-output`: A giant auto-generated snapshot that no one reviews is the core anti-pattern: it appears to test much and tests nothing (`yagni`, `explicit-over-implicit`).
- `must-normalize-non-deterministic-values`, `must-stabilize-ordering`, `should-use-property-matchers-for-dynamics`: Non-deterministic snapshots produce noisy diffs that train reviewers to accept blindly (`fail-fast` erodes when failures are routine).


- A fuzz target **MUST** accept raw bytes (or a deterministically derived structured input) and exercise exactly one parsing entry point.
- Harnesses **MUST** fail loudly: assert invariants and let sanitizers/panics surface defects (`fail-fast`).
- You **SHOULD** seed a starting corpus from real and edge-case samples; coverage grows far faster from good seeds.
- Every crash a fuzzer finds **MUST** be committed as a regression-corpus test case so the fix is permanently guarded.
- Long fuzzing campaigns **SHOULD** run in CI/nightly, not on the per-commit critical path; gate PRs on the seeded regression corpus and a short smoke run instead.


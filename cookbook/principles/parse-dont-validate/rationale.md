
- `should-encode-invariants-in-types`, `should-parse-at-the-boundary`, `should-make-illegal-states-unconstructable`: This is the structural form of fail-fast: the compiler rejects the bad case before it can run.
- `should-parse-at-the-boundary`, `should-not-revalidate-downstream`: Complements input-validation as a security control: validation rejects bad input; this principle ensures that what survives validation cannot later be misused.

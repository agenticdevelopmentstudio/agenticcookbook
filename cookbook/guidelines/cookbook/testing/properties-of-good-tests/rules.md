
- **must-isolate-test-vectors**: **Isolated** — each test vector MUST be independent; no shared mutable state or ordering dependency between vectors
- **must-make-expected-results-deterministic**: **Deterministic** — the expected result MUST be unambiguous; the same input always produces the same output
- **should-verify-behavior-not-internals**: **Behavioral** — test vectors SHOULD verify what the component does, not how it does it internally
- **should-target-one-behavior-per-vector**: **Specific** — each vector SHOULD target one behavior or edge case; a failure points to exactly one cause
- **must-make-vectors-readable**: **Readable** — a test vector MUST clearly communicate what it tests and what the expected outcome is
- **should-make-vector-set-predictive**: **Predictive** — the set of test vectors SHOULD be sufficient to catch real bugs; if all vectors pass, the implementation is likely correct

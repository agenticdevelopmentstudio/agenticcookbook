
- `must-isolate-test-vectors`: no shared mutable state or ordering dependency exists between any two test vectors
- `must-make-expected-results-deterministic`: every expected result is unambiguous and the same input always produces the same output
- `should-verify-behavior-not-internals`: whether the vectors verify what the component does, not how it does it internally
- `should-target-one-behavior-per-vector`: whether each vector targets one behavior or edge case
- `must-make-vectors-readable`: every vector clearly communicates what it tests and what the expected outcome is
- `should-make-vector-set-predictive`: whether the set of vectors is sufficient to catch real bugs

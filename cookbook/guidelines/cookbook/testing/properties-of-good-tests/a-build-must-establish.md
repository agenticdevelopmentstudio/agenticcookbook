
- `must-isolate-test-vectors`: every test vector is independent: none shares mutable state with or depends on the order of another
- `must-make-expected-results-deterministic`: every expected result is unambiguous, with one output per input
- `should-verify-behavior-not-internals`: the vectors check observable behavior, or any vector on internals is explained
- `should-target-one-behavior-per-vector`: each vector targets one behavior or edge case, so a failure points to one cause
- `must-make-vectors-readable`: every vector states what it tests and its expected outcome
- `should-make-vector-set-predictive`: the set of vectors is sufficient that passing all of them makes the implementation likely correct


- `must-isolate-test-vectors`: a vector that relies on state left by another vector, or on running in a set order
- `must-make-expected-results-deterministic`: an expected result that admits more than one reading, or that could differ for the same input
- `should-verify-behavior-not-internals`: a vector whose expected result names internal mechanics rather than what the component does
- `should-target-one-behavior-per-vector`: a vector that exercises several behaviors or edge cases at once, so a failure has more than one cause
- `must-make-vectors-readable`: a vector whose purpose or expected outcome cannot be read from it
- `should-make-vector-set-predictive`: a real bug the set of vectors would let pass

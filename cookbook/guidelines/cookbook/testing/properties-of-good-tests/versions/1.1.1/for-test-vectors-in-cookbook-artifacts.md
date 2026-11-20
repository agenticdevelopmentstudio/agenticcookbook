
1. **Isolated** — each test vector MUST be independent; no shared mutable state or ordering dependency between vectors
2. **Deterministic** — the expected result MUST be unambiguous; the same input always produces the same output
3. **Behavioral** — test vectors SHOULD verify what the component does, not how it does it internally
4. **Specific** — each vector SHOULD target one behavior or edge case; a failure points to exactly one cause
5. **Readable** — a test vector MUST clearly communicate what it tests and what the expected outcome is
6. **Predictive** — the set of test vectors SHOULD be sufficient to catch real bugs; if all vectors pass, the implementation is likely correct



- `should-give-high-complexity-algorithms-own-scope-group`: Code implementing O(n log n) or worse algorithms on large datasets is a distinct engineering concern — performance optimization, testing with large inputs, and benchmarking apply specifically to it.
- `should-treat-caching-layers-as-candidates`: A caching subsystem with its own eviction policy, invalidation logic, and hit/miss tracking is a meaningful independent component.
- `should-not-mix-computation-with-io`, `should-note-mixed-io-as-design-smell`: Files that mix algorithm implementation with network calls or file system access conflate two different concerns — note this as a design smell.
- `should-not-treat-crud-as-boundary-signal`: Code that maps data structures to/from persistence formats and performs no interesting computation is not algorithmically significant — its boundaries come from `module-boundaries` or `purpose-classification`.
- `must-scope-or-flag-parallel-computation`: Code using parallel execution primitives has distinct testing requirements (race conditions, thread safety) and likely belongs in its own scope group or must be flagged as a concurrency concern.


1. **High-complexity algorithms warrant their own scope group.** Code implementing O(n log n) or worse algorithms on large datasets is a distinct engineering concern — performance optimization, testing with large inputs, and benchmarking apply specifically to it.
2. **Caching layers are scope group candidates.** A caching subsystem with its own eviction policy, invalidation logic, and hit/miss tracking is a meaningful independent component.
3. **Computational code should not be mixed with I/O.** Files that mix algorithm implementation with network calls or file system access conflate two different concerns — note this as a design smell.
4. **Simple CRUD code is not a boundary signal.** Code that maps data structures to/from persistence formats and performs no interesting computation is not algorithmically significant — its boundaries come from `module-boundaries` or `purpose-classification`.
5. **Parallel computation implies a concurrency concern.** Code using parallel execution primitives has distinct testing requirements (race conditions, thread safety) and likely belongs in its own scope group or must be flagged as a concurrency concern.


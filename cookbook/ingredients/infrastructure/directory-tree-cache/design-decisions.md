
**Decision**: Store the cache as a flattened array rather than a nested tree.
**Rationale**: A flat array is simple to stream, tolerant of partial corruption per entry, and keeps the format independent of tree depth; parent-child wiring is cheap to rebuild from `parentPath`.
**Approved**: pending


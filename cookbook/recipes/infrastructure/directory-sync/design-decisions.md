
**Decision**: Split the lifecycle into a cache, a scanner, a watcher, and a thin coordinator instead of one monolithic coordinator.
**Rationale**: Each component has independent requirements and can be reused or replaced without touching the others; the coordinator owns only ordering, published state, and main-thread application. This replaces the earlier note that no design decisions had been recorded yet.
**Approved**: pending


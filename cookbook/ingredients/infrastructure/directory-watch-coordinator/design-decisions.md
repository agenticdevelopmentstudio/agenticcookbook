
**Decision**: The coordinator is a thin orchestrator over separate cache, scanner, and watcher ingredients.
**Rationale**: Each of those components has its own requirements and can be reused or replaced independently; the coordinator only owns ordering, published state, and main-thread application.
**Approved**: pending


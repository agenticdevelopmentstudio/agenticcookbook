
**Decision**: The handler is specified as its own ingredient rather than inside the worker.
**Rationale**: The worker is generic across job types; a handler is a unit that varies per job type. Keeping them separate lets new handlers be added without touching the worker contract.
**Approved**: pending


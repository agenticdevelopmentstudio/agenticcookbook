
The worker evaluates sync engine architecture: layered design (app → orchestrator → handlers → transport → local DB), entity-agnostic Syncable interface, explicit sync cycle steps (collect → package → send → receive → apply → checkpoint), sync scheduling logic, snapshot rebuilding, and error handling with circuit breaker patterns.



**Decision**: Split lifecycle into startup behavior, session restore, and child process cleanup.
**Rationale**: Each concern has its own settings, failure modes, and tests; the recipe states only their ordering.
**Approved**: pending

**Decision**: Save the restore list before child process cleanup runs.
**Rationale**: Cleanup can take up to the timeout and can be interrupted; the restore list is the more valuable artifact.
**Approved**: pending


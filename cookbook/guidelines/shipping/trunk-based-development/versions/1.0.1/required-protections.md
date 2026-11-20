
- **green-trunk**: Required status checks (build, tests, lint) MUST pass before any merge to trunk. Trunk MUST NOT be left red.
- **revertable-merges**: Each merge SHOULD be a single squashed commit so a regression can be reverted as one atomic unit.
- **no-freeze**: Integration MUST NOT be deferred to a batched "integration" or "stabilization" phase; integrate continuously.


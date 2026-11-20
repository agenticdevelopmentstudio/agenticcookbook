
- Sync direction specified: push-only, pull-only, or bidirectional (with justification)
- Incremental sync uses version cursors or change tracking (not full sync every time)
- All operations are idempotent (UPSERT semantics or explicit idempotency keys)
- Outbox pattern implemented for transactional consistency between local apply and remote acknowledgment
- Batch sync defined with pagination strategy for large changesets
- Retry strategy with exponential backoff specified (initial delay, max retries, backoff multiplier)
- `must-be-correct-under-network-failure`: A review passes when it establishes every item above.

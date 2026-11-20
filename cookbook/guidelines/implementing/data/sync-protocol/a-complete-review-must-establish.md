
- Sync direction specified: push-only, pull-only, or bidirectional (with justification)
- Incremental sync uses version cursors or change tracking (not full sync every time)
- All operations are idempotent (UPSERT semantics or explicit idempotency keys)
- Outbox pattern implemented for transactional consistency between local apply and remote acknowledgment
- Batch sync defined with pagination strategy for large changesets
- Retry strategy with exponential backoff specified (initial delay, max retries, backoff multiplier)
- Every MUST rule is kept, with no exception: `must-be-correct-under-network-failure`, `must-use-incremental-sync`, `must-set-dirty-on-every-local-write`, `must-build-sqlite-with-session-flags`, `must-paginate-sync-results`, `must-paginate-by-sync-version-cursor`, `must-make-sync-operations-replayable`, `must-guard-upserts-with-version`, `must-use-idempotency-keys`, `must-deduplicate-on-server`, `must-write-data-and-queue-atomically`, `must-back-off-with-jitter`, `must-not-retry-client-errors`, `must-not-retry-conflicts-blindly`
- Every SHOULD rule is kept, or the change says why not: `should-combine-push-and-pull`, `should-use-shoulder-tap`, `should-prefer-version-cursor-over-timestamps`, `should-use-hlc-for-timestamp-sync`, `should-clear-dirty-after-server-confirms`, `should-size-batches-by-context`, `should-classify-errors-before-retrying`, `should-retry-server-errors-with-longer-backoff`, `should-enter-circuit-breaker`


A review passes when it establishes every item above.

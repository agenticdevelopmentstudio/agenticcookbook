
- Sync layers defined and documented (application layer, sync orchestrator, entity handlers, transport, local DB)
- Syncable interface documented with required methods (getDirtyChanges, applyRemoteChanges, getCheckpoint, etc.)
- Sync cycle steps explicit and ordered: collect changes → package → send → receive → apply → checkpoint
- Sync scheduling strategy documented (interval, exponential backoff, on-demand, connectivity-triggered)
- Snapshot rebuilding mechanism specified for consistency verification
- Error classification documented (transient vs permanent) with handling strategy per type
- Circuit breaker thresholds defined (failure count, timeout duration, reset strategy)
- Every rule is kept, or the change says why not: `should-separate-four-layers`, `must-read-application-from-local-sqlite`, `should-implement-syncable-interface`, `may-customize-conflict-handling-per-type`, `should-complete-cycle-in-one-round-trip`, `should-rebuild-derived-state-before-notifying-ui`, `should-start-with-is-dirty-flags`, `must-set-dirty-on-every-local-write`, `should-clear-dirty-after-successful-sync`, `should-use-change-log-only-for-operation-awareness`, `should-use-edit-operations-only-for-three-way-merge`, `should-implement-two-scheduling-modes`, `must-throttle-event-driven-sync`, `must-rebuild-snapshots-in-dependency-order`, `must-back-off-with-jitter-on-transient-failures`, `must-not-retry-client-errors`, `should-resolve-409-then-retry`, `should-retry-500-with-longer-backoff`, `should-break-circuit-after-consecutive-failures`, `should-log-sync-failure-reason`, `must-surface-persistent-sync-failures`


A review passes when it establishes every item above.


- WAL mode enabled on local SQLite database for offline capability
- Local-first read/write with background sync to server
- Operation queue pattern implemented for mutations queued while offline
- Optimistic UI updates with rollback path when server rejects operation
- Schema migration strategy handles offline devices (deferred, conditional, or dual schema)
- Data expiry and cache invalidation strategy documented
- Connectivity detection implemented to trigger sync when connection restored
- Every MUST rule is kept, with no exception: `must-enable-wal-for-synced-databases`, `must-not-hold-write-transaction-during-network-io`, `must-write-mutation-and-outbox-atomically`, `must-read-ui-from-local-sqlite`, `must-roll-back-on-server-rejection`, `must-run-migrations-regardless-of-network`, `must-only-add-columns`, `must-give-new-columns-defaults`, `must-make-migrations-idempotent`, `must-wrap-migration-steps-in-transactions`, `must-test-migrations-from-every-version`, `must-adjust-sync-to-connectivity`, `must-not-retry-sync-in-tight-loop`
- Every SHOULD rule is kept, or the change says why not: `should-use-synchronous-full-only-for-power-loss-safety`, `should-use-one-writer-many-readers`, `should-design-ui-for-server-rejection`, `should-track-schema-version-with-user-version`, `should-recreate-table-for-complex-migrations`, `should-prune-sync-metadata-on-schedule`, `should-incremental-vacuum-after-significant-deletions`, `should-trigger-periodic-full-sync`, `should-back-off-from-first-failure`


A review passes when it establishes every item above.

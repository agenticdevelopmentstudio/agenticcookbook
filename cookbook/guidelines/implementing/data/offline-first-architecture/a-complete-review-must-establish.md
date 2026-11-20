
- WAL mode enabled on local SQLite database for offline capability
- Local-first read/write with background sync to server
- Operation queue pattern implemented for mutations queued while offline
- Optimistic UI updates with rollback path when server rejects operation
- Schema migration strategy handles offline devices (deferred, conditional, or dual schema)
- Data expiry and cache invalidation strategy documented
- Connectivity detection implemented to trigger sync when connection restored
- Every rule is kept, or the change says why not: `must-enable-wal-for-synced-databases`, `should-use-synchronous-full-only-for-power-loss-safety`, `should-use-one-writer-many-readers`, `must-not-hold-write-transaction-during-network-io`, `must-write-mutation-and-outbox-atomically`, `must-read-ui-from-local-sqlite`, `should-design-ui-for-server-rejection`, `must-roll-back-on-server-rejection`, `must-run-migrations-regardless-of-network`, `should-track-schema-version-with-user-version`, `should-recreate-table-for-complex-migrations`, `must-only-add-columns`, `must-give-new-columns-defaults`, `must-make-migrations-idempotent`, `must-wrap-migration-steps-in-transactions`, `must-test-migrations-from-every-version`, `should-prune-sync-metadata-on-schedule`, `should-incremental-vacuum-after-significant-deletions`, `should-trigger-periodic-full-sync`, `must-adjust-sync-to-connectivity`, `must-not-retry-sync-in-tight-loop`, `should-back-off-from-first-failure`


A review passes when it establishes every item above.

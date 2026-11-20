
- WAL mode enabled (PRAGMA journal_mode = WAL)
- Write transactions use BEGIN IMMEDIATE; read transactions use BEGIN DEFERRED
- busy_timeout set to reasonable value (e.g., 5000ms) to prevent SQLITE_BUSY errors
- Production PRAGMAs configured: synchronous=NORMAL, cache_size=-64000, journal_size_limit, foreign_keys=ON
- Connection pooling implements single-writer pattern for write transactions
- Transaction isolation levels understood and documented for concurrent read scenarios
- Every MUST rule is kept, with no exception: `must-enable-wal-mode`, `must-keep-wal-processes-on-one-machine`, `must-not-use-wal-on-network-file-systems`, `must-not-change-page-size-after-wal`, `must-not-use-memory-or-off-journal-in-production`, `must-wrap-write-batches-in-transactions`, `must-use-begin-immediate-for-writes`, `must-set-busy-timeout`, `must-not-hold-write-lock-during-external-io`, `must-restore-safe-settings-after-bulk-load`, `must-not-use-bulk-load-settings-in-production`
- Every SHOULD rule is kept, or the change says why not: `should-set-wal-on-connection-open`, `should-lower-busy-timeout-for-interactive-ui`, `should-set-recommended-pragmas-on-every-connection`, `should-use-single-writer-many-readers`, `should-keep-write-transactions-short`, `should-run-passive-checkpoints-periodically`, `should-truncate-checkpoint-after-large-batches`, `should-cap-wal-size`, `should-not-disable-auto-checkpoint-without-replacement`, `should-not-hold-long-read-transactions`, `should-not-run-very-large-write-transactions`, `should-checkpoint-off-the-foreground`


A review passes when it establishes every item above.

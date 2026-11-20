
- Backup strategy chosen and documented: SQLite backup API or Litestream for continuous replication
- PRAGMA integrity_check scheduled and run periodically; failures trigger alerts
- VACUUM strategy selected (incremental PRAGMA incremental_vacuum for ongoing cleanup, or full VACUUM with size threshold)
- Database size monitoring in place with alerts for growth anomalies
- Tombstone retention window defined (e.g., keep soft-deleted records for 30 days before purging)
- Recovery procedure documented and tested; recovery RTO/RPO defined
- Every MUST rule is kept, with no exception: `must-use-litestream-for-point-in-time-recovery`, `must-not-sync-writers-with-litestream`, `must-delete-wal-and-shm-before-restore`, `must-not-run-on-network-filesystems`, `must-not-delete-journal-files-while-open`, `must-coordinate-writers-through-sqlite-locking`, `must-not-move-database-without-journal`, `must-not-disable-durability-pragmas-in-production`, `must-set-auto-vacuum-incremental-at-creation`, `must-have-free-space-for-full-vacuum`, `must-not-vacuum-under-write-load`, `must-purge-tombstones-only-after-all-targets-sync`
- Every SHOULD rule is kept, or the change says why not: `should-choose-backup-method-by-durability-needs`, `should-have-tested-recovery-path`, `should-use-normal-or-full-synchronous`, `should-check-integrity-on-schedule`, `should-quick-check-critical-databases-on-startup`, `should-reserve-integrity-check-for-offline-audits`, `should-prefer-incremental-vacuum`, `should-vacuum-during-idle-time`, `should-monitor-database-size`, `should-alert-on-free-page-ratio`, `should-define-retention-windows-from-the-start`, `should-incremental-vacuum-after-large-purges`


A review passes when it establishes every item above.

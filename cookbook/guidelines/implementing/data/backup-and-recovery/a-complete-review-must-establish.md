
- Backup strategy chosen and documented: SQLite backup API or Litestream for continuous replication
- PRAGMA integrity_check scheduled and run periodically; failures trigger alerts
- VACUUM strategy selected (incremental PRAGMA incremental_vacuum for ongoing cleanup, or full VACUUM with size threshold)
- Database size monitoring in place with alerts for growth anomalies
- Tombstone retention window defined (e.g., keep soft-deleted records for 30 days before purging)
- Recovery procedure documented and tested; recovery RTO/RPO defined
- `should-have-tested-recovery-path`: A review passes when it establishes every item above.

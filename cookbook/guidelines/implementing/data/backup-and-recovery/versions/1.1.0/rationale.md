
- `must-delete-wal-and-shm-before-restore`: A stale or mismatched WAL file will corrupt the restored database. The WAL and database file are a matched pair — they cannot be mixed.
- `must-purge-tombstones-only-after-all-targets-sync`: Purging too early causes deleted records to reappear on devices that haven't synced yet.


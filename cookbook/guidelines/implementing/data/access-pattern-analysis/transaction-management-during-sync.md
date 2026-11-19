
```python
def apply_sync_batch(changes, db):
    db.execute("BEGIN IMMEDIATE")
    try:
        for change in changes:
            apply_change(db, change)
        db.execute("COMMIT")
    except Exception:
        db.execute("ROLLBACK")
        raise
```

The pattern is: fetch the batch from the server, then open the transaction, apply all changes, commit. Network I/O happens outside the transaction boundary.

**Connection separation for sync:**
- One dedicated write connection for sync writes (prevents `SQLITE_BUSY` from competing writers)
- Separate read connections for UI queries that run during sync
- Set `busy_timeout = 5000` on all connections to absorb brief contention without returning errors

This connection strategy, combined with WAL mode, allows the sync writer to apply batches while the UI continues to read — the fundamental concurrency requirement for a responsive offline-first application.


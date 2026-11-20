
**Single writer, multiple readers:**
- One dedicated write connection with an application-level queue
- Multiple read connections for concurrent UI or background queries
- Never hold a write transaction open while waiting for network I/O

```python
# Sync workload pattern
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


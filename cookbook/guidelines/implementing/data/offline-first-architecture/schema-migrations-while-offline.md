
Devices may be offline when a new app version with schema changes ships. Migrations MUST run successfully regardless of network state.

Use `PRAGMA user_version` to track the applied schema version:

```python
def migrate(db):
    version = db.execute("PRAGMA user_version").fetchone()[0]
    if version < 1:
        db.execute("ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'medium'")
        db.execute("PRAGMA user_version = 1")
    if version < 2:
        db.execute("BEGIN TRANSACTION")
        # For complex changes: create new table, copy, drop old
        db.execute("COMMIT")
        db.execute("PRAGMA user_version = 2")
```

Rules for sync-compatible migrations:

1. MUST only add columns — never remove or rename without a migration path
2. New columns MUST have DEFAULT values (required by CRDTs and outbox replay)
3. Migrations MUST be idempotent (safe to run twice)
4. MUST wrap each migration step in a transaction
5. MUST test migrations against databases at every previous schema version


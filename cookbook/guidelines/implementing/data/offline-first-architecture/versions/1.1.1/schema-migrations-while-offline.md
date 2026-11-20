
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


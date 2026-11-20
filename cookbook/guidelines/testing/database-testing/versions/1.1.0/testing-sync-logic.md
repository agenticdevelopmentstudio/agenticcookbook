
Change detection:

```python
def test_detects_unsynced_records(db):
    # insert a record but do not mark it synced
    db.execute("INSERT INTO tasks (id, title, updated_at) VALUES (?, ?, ?)",
               ('t1', 'Task', '2026-04-06T00:00:00Z'))
    rows = db.execute(
        "SELECT id FROM tasks WHERE last_synced_at IS NULL OR updated_at > last_synced_at"
    ).fetchall()
    assert ('t1',) in rows
```


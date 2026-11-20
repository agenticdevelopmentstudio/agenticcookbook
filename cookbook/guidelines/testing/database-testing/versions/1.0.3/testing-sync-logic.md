
Sync logic requires testing at the unit level (change detection, serialization) and integration level (round-trip apply).

**Change detection**: verify that the unsynced-records query returns the correct rows.

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

**Sync apply**: verify that applying a changeset from the server updates the local database correctly, including soft-delete propagation.

**Outbox round-trip**: write a record locally, confirm it appears in the outbox, simulate a sync cycle, confirm the record is marked synced and the outbox entry is consumed.

**Tombstone propagation**: delete a record on one simulated peer, apply the tombstone to a second peer, confirm the record is absent on the second peer and not resurrected by a subsequent sync.


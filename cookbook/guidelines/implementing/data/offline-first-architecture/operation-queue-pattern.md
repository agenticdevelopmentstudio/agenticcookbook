
Every user mutation MUST be written to both the data table and an outbox queue in a single atomic transaction. This guarantees that whatever is visible on screen is queued for sync.

```python
db.execute("BEGIN TRANSACTION")
db.execute(
    "INSERT INTO tasks (id, title, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
    [task_id, title, "pending", now, now]
)
db.execute(
    "INSERT INTO outbox (id, type, payload, idempotency_key, status, created_at) "
    "VALUES (?, 'create_task', ?, ?, 'pending', ?)",
    [queue_id, json.dumps(task_data), f"create_task:{task_id}", now]
)
db.execute("COMMIT")
```

An event-sourcing variant stores the operation rather than a snapshot:

```json
{"type": "task_created", "task_id": "abc", "title": "Buy groceries"}
{"type": "task_status_changed", "task_id": "abc", "status": "done"}
```

The server replays these events to reconstruct state. This approach naturally supports undo/redo and makes sync equivalent to event replay.


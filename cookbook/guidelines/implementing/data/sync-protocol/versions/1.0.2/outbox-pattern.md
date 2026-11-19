
MUST write to the local data table and the sync queue in a single transaction. This guarantees the outbox always reflects local state — there is no window where a change is visible on screen but not queued for sync.

```python
db.execute("BEGIN TRANSACTION")

db.execute(
    "INSERT INTO tasks (id, title, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
    [task_id, title, status, now, now]
)
db.execute(
    "INSERT INTO sync_queue (id, idempotency_key, operation, table_name, record_id, payload) "
    "VALUES (?, ?, 'INSERT', 'tasks', ?, ?)",
    [queue_id, f"insert:tasks:{task_id}", task_id, json.dumps(task_data)]
)

db.execute("COMMIT")
# If the task is on screen, it is in the outbox.
```

The sync worker processes the queue asynchronously, retrying failed entries with exponential backoff. Completed entries can be pruned after a retention window (e.g., 7 days for debugging).


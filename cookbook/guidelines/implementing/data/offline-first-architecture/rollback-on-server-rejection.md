
MUST implement rollback when the server rejects an optimistic write. Silently ignoring rejections causes local and server state to diverge permanently.

```python
def handle_rejection(outbox_entry, server_response):
    db.execute("BEGIN TRANSACTION")
    if outbox_entry.type == "create_task":
        db.execute("DELETE FROM tasks WHERE id = ?", [outbox_entry.record_id])
    elif outbox_entry.type == "update_task":
        # Restore the server's authoritative version
        apply_server_version(server_response.current_record)
    db.execute(
        "UPDATE outbox SET status = 'failed' WHERE id = ?",
        [outbox_entry.id]
    )
    db.execute("COMMIT")
    notify_user("Change could not be saved: " + server_response.reason)
```


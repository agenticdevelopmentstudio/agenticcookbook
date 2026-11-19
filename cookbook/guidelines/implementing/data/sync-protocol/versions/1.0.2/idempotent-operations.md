
Every sync operation MUST be safe to replay. Network failures mean the same batch may be delivered multiple times.

Use UPSERT with a version guard so replaying an older batch never downgrades a record:

```sql
INSERT INTO tasks (id, title, status, updated_at, version)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT (id) DO UPDATE SET
    title      = EXCLUDED.title,
    status     = EXCLUDED.status,
    updated_at = EXCLUDED.updated_at,
    version    = EXCLUDED.version
WHERE EXCLUDED.version > tasks.version;
```

Use **idempotency keys** in the outbox to prevent duplicate processing on the server:

```sql
CREATE TABLE sync_queue (
    id               TEXT PRIMARY KEY,
    idempotency_key  TEXT NOT NULL UNIQUE,   -- deterministic: "insert:tasks:<id>"
    operation        TEXT NOT NULL,
    table_name       TEXT NOT NULL,
    record_id        TEXT NOT NULL,
    payload          TEXT NOT NULL,
    status           TEXT NOT NULL DEFAULT 'pending',
    attempt_count    INTEGER NOT NULL DEFAULT 0,
    next_attempt_at  INTEGER NOT NULL DEFAULT 0,
    created_at       TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- Prevent duplicates on retry
INSERT OR IGNORE INTO sync_queue (id, idempotency_key, operation, table_name, record_id, payload)
VALUES (?, ?, ?, ?, ?, ?);
```

The server MUST also deduplicate on idempotency key and return success (not an error) for already-processed requests.


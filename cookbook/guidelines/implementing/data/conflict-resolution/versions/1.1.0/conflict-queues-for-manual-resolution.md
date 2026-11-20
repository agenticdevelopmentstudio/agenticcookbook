
```sql
CREATE TABLE sync_conflicts (
    id            TEXT PRIMARY KEY NOT NULL,
    table_name    TEXT NOT NULL,
    record_id     TEXT NOT NULL,
    client_data   TEXT NOT NULL,   -- JSON of client version
    server_data   TEXT NOT NULL,   -- JSON of server version
    base_data     TEXT,            -- JSON of last-synced version (for 3-way merge)
    conflict_type TEXT NOT NULL,   -- 'update_update', 'update_delete', 'delete_update'
    detected_at   TEXT NOT NULL,
    resolved_at   TEXT,
    resolution    TEXT,            -- 'client', 'server', 'merged', 'discarded'
    resolved_data TEXT
);

CREATE INDEX idx_conflicts_unresolved
ON sync_conflicts(resolved_at) WHERE resolved_at IS NULL;
```


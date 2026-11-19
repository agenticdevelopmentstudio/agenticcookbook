
Add a `sync_state` table (or equivalent) to store per-device checkpoint information:

```sql
CREATE TABLE sync_state (
    key     TEXT PRIMARY KEY NOT NULL,  -- e.g. 'last_sync_version', 'device_id'
    value   TEXT NOT NULL
);
```


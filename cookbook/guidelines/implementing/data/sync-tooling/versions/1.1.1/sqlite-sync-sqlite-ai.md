
A CRDT-based loadable extension that syncs SQLite with SQLite Cloud, PostgreSQL, and Supabase.

```sql
.load cloudsync
SELECT cloudsync_init('tasks');
INSERT INTO tasks (id, title) VALUES (cloudsync_uuid(), 'New task');
SELECT cloudsync_network_init('your-database-id');
SELECT cloudsync_network_set_apikey('your-api-key');
SELECT cloudsync_network_sync();
```

Supports multiple CRDT algorithms per table: `cls` (Causal-Length Set, default), `dws` (Delete-Wins), `aws` (Add-Wins), `gos` (Grow-Only). Text columns support block-level LWW for per-line conflict resolution.

**Schema requirements:** All NOT NULL columns must have DEFAULT values. TEXT primary keys with UUIDv7 required. ALTER TABLE requires wrapping with `cloudsync_begin_alter` / `cloudsync_commit_alter`.

**Use when:** You want automatic CRDT-based sync with minimal code against SQLite Cloud, Postgres, or Supabase, and can accept Beta maturity.


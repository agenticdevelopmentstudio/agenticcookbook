
UUIDs enable client-side ID generation without server coordination, which is essential for offline-first sync. Without UUIDs, two offline devices using autoincrement will produce identical IDs that collide on sync.

**Recommended: UUIDv7 (time-ordered)**

UUIDv7 encodes a Unix millisecond timestamp in the first 48 bits, making IDs roughly time-ordered. This preserves B-tree locality while maintaining global uniqueness. UUIDv4 (random) scatters inserts across the entire tree, causing page splits and cache thrashing.

```sql
-- Store UUIDv7 as BLOB for maximum efficiency (16 bytes vs 36 for TEXT)
CREATE TABLE distributed_events (
    event_id BLOB PRIMARY KEY,
    payload  TEXT NOT NULL
) WITHOUT ROWID;
```

**SQLite-specific note:** Unlike PostgreSQL, SQLite's clustered index is the rowid, not the PK column. A TEXT UUID primary key creates a separate B-tree — UUID randomness therefore causes less fragmentation than in PostgreSQL.

**For internal + external IDs, use a hybrid approach:**

```sql
CREATE TABLE resources (
    resource_id  INTEGER PRIMARY KEY,    -- fast internal FK target
    external_id  TEXT NOT NULL UNIQUE,  -- UUIDv7 for API / sync
    resource_name TEXT NOT NULL
);
```

**Never use `INTEGER PRIMARY KEY AUTOINCREMENT` for synced tables.** IDs will collide across devices.


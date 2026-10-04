
A fork of SQLite with built-in replication and embedded replicas. The remote Turso database is the source of truth; each device holds a local SQLite copy for zero-latency reads.

Sync uses frame-based WAL replication. Supports manual sync (`client.sync()`), periodic polling (`syncInterval`), and offline writes pushed on reconnection.

**Conflict resolution options:**
- `DISCARD_LOCAL` — server-wins
- `REBASE_LOCAL` — replay local changes on top of server state
- `FAIL_ON_CONFLICT` — reject and surface to application
- `MANUAL_RESOLUTION` — callback with both versions

**Limitations:** Offline write sync is Beta maturity. Requires Turso Cloud as the server; not compatible with arbitrary Postgres backends.

**Use when:** You want embedded SQLite replicas with managed server infrastructure and are comfortable with Turso Cloud as your backend.


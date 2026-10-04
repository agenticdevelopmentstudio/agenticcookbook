
MUST use UUID primary keys for all synced tables. Never use `INTEGER PRIMARY KEY AUTOINCREMENT` for synced tables — auto-incremented integers are generated locally by each device and will collide across devices when syncing.

Use **UUIDv7** (time-ordered) where possible. UUIDv7 embeds a timestamp prefix, preserving roughly-chronological insert ordering while guaranteeing global uniqueness. PostgreSQL 17+ supports `gen_random_uuid()` or `uuid_generate_v7()`.

```sql
-- SQLite: sync-ready table
CREATE TABLE tasks (
    id          TEXT    PRIMARY KEY NOT NULL,   -- UUIDv7, generated client-side
    title       TEXT    NOT NULL,
    status      TEXT    NOT NULL DEFAULT 'pending',
    created_at  TEXT    NOT NULL,               -- ISO-8601 UTC
    updated_at  TEXT    NOT NULL,               -- ISO-8601 UTC
    version     INTEGER NOT NULL DEFAULT 1,
    is_deleted  INTEGER NOT NULL DEFAULT 0,
    last_synced_at TEXT                         -- NULL until first sync
);

-- PostgreSQL: corresponding server table
CREATE TABLE tasks (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    title       TEXT        NOT NULL,
    status      TEXT        NOT NULL DEFAULT 'pending',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    version     INTEGER     NOT NULL DEFAULT 1,
    is_deleted  BOOLEAN     NOT NULL DEFAULT FALSE,
    last_synced_at TIMESTAMPTZ
);
```


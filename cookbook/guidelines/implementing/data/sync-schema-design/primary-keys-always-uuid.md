
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

PostgreSQL 17+ supports `gen_random_uuid()` or `uuid_generate_v7()`.


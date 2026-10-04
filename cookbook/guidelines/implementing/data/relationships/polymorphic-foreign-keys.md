
A polymorphic FK references one of several different tables. A common example: an audit log where the actor could be a human, a service, or a bot.

### Pattern 1: Generic FK with discriminator column

```sql
CREATE TABLE audit_log (
    audit_log_id    INTEGER PRIMARY KEY,
    changed_by_id   INTEGER NOT NULL,
    changed_by_type TEXT NOT NULL CHECK (changed_by_type IN ('human', 'service', 'bot'))
);
```

Simple, works everywhere. SQLite cannot enforce FK integrity across multiple tables even with `PRAGMA foreign_keys = ON` — the application owns that constraint. Easy to get into an inconsistent state without discipline.

### Pattern 2: Supertype / base table (recommended)

```sql
CREATE TABLE actors (
    actor_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    actor_type   TEXT NOT NULL CHECK (actor_type IN ('human', 'service', 'bot')),
    display_name TEXT NOT NULL  -- denormalized for fast queries
);

CREATE TABLE humans (
    actor_id INTEGER PRIMARY KEY REFERENCES actors(actor_id),
    email    TEXT NOT NULL UNIQUE
);

CREATE TABLE services (
    actor_id     INTEGER PRIMARY KEY REFERENCES actors(actor_id),
    service_name TEXT NOT NULL
);

CREATE TABLE audit_log (
    audit_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    changed_by   INTEGER NOT NULL REFERENCES actors(actor_id),
    change_date  TEXT NOT NULL DEFAULT (datetime('now'))
);
```

`audit_log.changed_by` is a real, enforced FK into the supertype table. Each subtype has a 1:1 FK back to the supertype. Denormalize `display_name` onto the supertype to avoid subtype joins for common display queries.

**Use Pattern 2** when actor types share a common identity concept and referential integrity matters. **Use Pattern 1** when moving fast and comfortable enforcing integrity in application code.

### Pattern 3: Nullable column per type

```sql
CREATE TABLE audit_log (
    audit_log_id           INTEGER PRIMARY KEY,
    changed_by_human_id    INTEGER REFERENCES humans(actor_id),
    changed_by_service_id  INTEGER REFERENCES services(actor_id),
    CHECK (
        (changed_by_human_id   IS NOT NULL) +
        (changed_by_service_id IS NOT NULL) = 1
    )
);
```

Gives real FK enforcement on each column. Gets unwieldy when types grow beyond 3–4.


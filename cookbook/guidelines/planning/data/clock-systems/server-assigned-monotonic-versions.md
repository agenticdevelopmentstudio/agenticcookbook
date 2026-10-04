
Instead of relying on client clocks, the server assigns a strictly increasing version number to every accepted change using a database sequence.

```sql
-- PostgreSQL: monotonic sync version sequence
CREATE SEQUENCE sync_version_seq;

-- On every write accepted during sync:
UPDATE tasks
SET sync_version = nextval('sync_version_seq')
WHERE id = ?;
```

**Properties:**
- Zero clock-skew issues — the server is the sole authority on ordering
- Clients request delta pulls with `WHERE sync_version > ?` — simple and efficient
- Easy to reason about and debug
- Requires server connectivity to assign versions — not suitable for pure peer-to-peer

**When to use:** Client-server architectures where all writes are validated by the server. This is the most common pattern in production sync systems (Linear, Figma, and most mobile apps use variants of this). SHOULD be the default choice for centralized sync.


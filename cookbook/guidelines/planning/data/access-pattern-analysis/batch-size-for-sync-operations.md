
Batch size is an access pattern decision: too small, and HTTP overhead dominates; too large, and a failed request wastes work.

| Context | Recommended Batch Size | Rationale |
|---------|----------------------|-----------|
| Mobile (unstable network) | 50–100 records | Smaller batches survive connection drops |
| Desktop (stable network) | 500–1,000 records | Reduces HTTP round-trips |
| Initial bootstrap | 1,000–5,000 records | Fast initial sync is critical for UX |
| Background sync | 100–500 records | Balances throughput with UI responsiveness |

MUST wrap each sync batch in a single transaction. Applying changes row-by-row in autocommit mode pays an fsync per row — at 30ms+ per fsync, a 500-record batch would take 15 seconds.

```sql
BEGIN IMMEDIATE;
-- apply all changes in the batch
COMMIT;
```

For bulk ingestion (initial sync or large imports), use JSON bulk operations to avoid SQLite's per-statement parameter limit and reduce round-trips:

```sql
-- Bulk insert via JSON: single statement for an entire batch
INSERT INTO tasks (id, title, status)
SELECT e->>'id', e->>'title', e->>'status'
FROM json_each(?) e;
```


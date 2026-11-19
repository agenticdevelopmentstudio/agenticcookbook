
Every SQL statement runs in a transaction. Without an explicit `BEGIN`, each statement gets its own implicit transaction with a separate fsync.

```sql
-- SLOW: each INSERT triggers an fsync (30ms+ per statement)
INSERT INTO t VALUES (1);
INSERT INTO t VALUES (2);
INSERT INTO t VALUES (3);

-- FAST: one fsync for all three
BEGIN;
INSERT INTO t VALUES (1);
INSERT INTO t VALUES (2);
INSERT INTO t VALUES (3);
COMMIT;
```

MUST wrap batches of writes in explicit transactions. Even a modest batch (10–100 rows) benefits significantly.

**Optimal batch size:**
- General use: 100–1,000 rows per transaction
- Bulk loading: 10,000–100,000 rows per transaction
- Sync batches: 50–500 records (smaller on unstable networks)


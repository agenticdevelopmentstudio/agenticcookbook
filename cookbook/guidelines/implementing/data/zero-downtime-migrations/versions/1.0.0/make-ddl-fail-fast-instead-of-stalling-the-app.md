
A blocking DDL statement that waits on a lock will queue *behind* it every subsequent query on that table — the app appears frozen. Bound the wait so a contended migration aborts cleanly and can be retried.

- Migrations that take table locks **MUST** set `lock_timeout` (e.g. `SET lock_timeout = '5s'`) so a blocked `ALTER`/`DROP` fails fast rather than building a lock queue. Set `statement_timeout` too, to bound the statement's own runtime.
- A migration that aborts on `lock_timeout` **SHOULD** be retried with backoff rather than run unbounded.
- Indexes on large live tables **MUST** be built with `CREATE INDEX CONCURRENTLY` (and dropped with `DROP INDEX CONCURRENTLY`) to avoid an `ACCESS EXCLUSIVE` lock on writes.
- `CREATE INDEX CONCURRENTLY` cannot run inside a transaction block. Migration steps that use it **MUST NOT** be wrapped in a transaction, and the step **SHOULD** check for and clean up an `INVALID` index left by a failed concurrent build before retrying.

```sql
-- Expand: safe, non-blocking
SET lock_timeout = '5s';
ALTER TABLE orders ADD COLUMN customer_uuid uuid;          -- nullable, instant
CREATE INDEX CONCURRENTLY idx_orders_customer_uuid          -- no transaction wrapper
  ON orders (customer_uuid);
```


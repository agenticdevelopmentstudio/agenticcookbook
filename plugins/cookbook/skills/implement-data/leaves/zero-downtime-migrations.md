<!-- leaf: implement-data/zero-downtime-migrations · source: guidelines/implementing/data/zero-downtime-migrations.md -->

**Rules** (cite as `implement-data/zero-downtime-migrations#<slug>`):

- `migration-step-compatible-app-version-currently` MUST — Each migration step MUST be compatible with the app version currently running against it — both N-1 and N must function …
- `change-code-depends-not-ship-same-atomic-step` MUST — A schema change and the code that depends on it MUST NOT ship in the same atomic step. The schema goes first …
- `type-add-null-deferred-contract-phase-after` MUST — Destructive changes (drop column, rename, narrow a type, add NOT NULL) MUST be deferred to the contract phase, after no …
- `new-columns-added-nullable-safe-default` MUST — New columns MUST be added as nullable or with a safe default; do not add NOT NULL to an existing large table in one …
- `renames-done-add-new-dual` MUST — Renames MUST be done as add-new + dual-write + backfill + switch + drop-old, never as an in-place RENAME that breaks …
- `backfills-run-bounded-batches-primary` MUST — Backfills MUST run in bounded batches (e.g. by primary-key range) with a commit per batch, so they hold no long …
- `backfill-jobs-idempotent-so-re-run` SHOULD — Backfill jobs SHOULD be idempotent so a re-run after partial failure produces the same result.
- `take-table-locks-set-lock-timeout-set` MUST — Migrations that take table locks MUST set lock_timeout (e.g. SET lock_timeout = '5s') so a blocked ALTER/DROP fails …
- `aborts-lock-timeout-retried-backoff-rather-than` SHOULD — A migration that aborts on lock_timeout SHOULD be retried with backoff rather than run unbounded.
- `large-live-tables-built-create-index-concurrently` MUST — Indexes on large live tables MUST be built with CREATE INDEX CONCURRENTLY (and dropped with DROP INDEX CONCURRENTLY) to …
- `migration-steps-use-not-wrapped-transaction-step-check` MUST — CREATE INDEX CONCURRENTLY cannot run inside a transaction block. Migration steps that use it MUST NOT be wrapped in a …
- `old-shape-survive-least-one-full` MUST — The old shape MUST survive at least one full deploy cycle past the switch so any in-flight N-1 instances stay …

# Zero-downtime migrations: expand and contract

When the database is serving live traffic, a migration cannot pause the app or rewrite a whole table in place. Split every schema change into small, individually-deployable, backward-compatible steps so the running app version keeps working at all times. This is the opposite of an offline table-recreate (e.g. SQLite's 12-step rebuild), which assumes nobody is reading the table.

## The core invariant: N / N-1 compatibility

During a rolling deploy, both the old app version (N-1) and the new one (N) run against the *same* schema simultaneously.

- Each migration step **MUST** be compatible with the app version currently running against it — both N-1 and N must function after the step is applied.
- A schema change and the code that depends on it **MUST NOT** ship in the same atomic step. The schema goes first (additive), code follows, cleanup goes last.
- Destructive changes (drop column, rename, narrow a type, add NOT NULL) **MUST** be deferred to the contract phase, after no running code references the old shape.

## Expand and contract (parallel change)

Spread one logical change across multiple releases:

| Phase | Action | Compatibility |
|-------|--------|---------------|
| **Expand** | Add new column/table/index. Make it nullable or defaulted. | Old code ignores it; new code may use it |
| **Migrate** | Dual-write (app writes old + new) and backfill existing rows in batches | Reads still served from old shape |
| **Switch** | Move reads to the new shape once backfill is complete and verified | New code reads new; old code still reads old |
| **Contract** | Stop dual-writing, drop the old column/table/index | Only run after no deployed version uses the old shape |

- New columns **MUST** be added as nullable or with a safe default; do not add `NOT NULL` to an existing large table in one step. Add the column, backfill, then add the constraint as `NOT VALID` and `VALIDATE CONSTRAINT` separately.
- Renames **MUST** be done as add-new + dual-write + backfill + switch + drop-old, never as an in-place `RENAME` that breaks N-1.
- Backfills **MUST** run in bounded batches (e.g. by primary-key range) with a commit per batch, so they hold no long transaction and can resume after interruption.
- Backfill jobs **SHOULD** be idempotent so a re-run after partial failure produces the same result.

## Make DDL fail fast instead of stalling the app

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

## Roll back by reversing, not undoing

- Because each step is additive and backward-compatible, the rollback is to **redeploy the previous app version** — the expanded schema still works for it. Avoid down-migrations that drop just-added columns during an incident; they re-introduce the lock you were avoiding.
- The old shape **MUST** survive at least one full deploy cycle past the switch so any in-flight N-1 instances stay functional.

> Note: exact lock behavior and which `ALTER TABLE` operations rewrite the table vary by database engine and version. The Postgres examples here are illustrative; confirm against your engine's current `ALTER TABLE` documentation before relying on a clause being non-blocking.

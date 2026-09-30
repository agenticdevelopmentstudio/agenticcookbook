<!-- leaf: implement-data/transaction-isolation · source: guidelines/implementing/data/transaction-isolation.md -->

**Rules** (cite as `implement-data/transaction-isolation#<slug>`):

- `writer-model-code-choose-isolation-level-deliberately` MUST — Multi-writer databases (PostgreSQL, MySQL/InnoDB, SQL Server, CockroachDB) use snapshot-based concurrency where …
- `deliberate-level` MUST
- `retry-serialization-failure` MUST
- `bounded-backoff` MUST
- `idempotent-retry` MUST
- `no-savepoint-only-retry` MUST
- `explicit-locking-for-queues` MUST
- `prefer-narrowest-level` SHOULD
- `expected-under-contention-retried` MUST — Treating 40001 as a hard error and surfacing it to the user — it is expected under contention and MUST be retried.

# Transaction isolation and serialization-failure retry

Multi-writer databases (PostgreSQL, MySQL/InnoDB, SQL Server, CockroachDB) use snapshot-based concurrency where transactions can conflict at commit time. Unlike SQLite's single-writer model, code MUST choose an isolation level deliberately and retry the serialization failures that stronger levels can raise.

## Isolation levels and what they prevent

Mapped to the SQL standard; PostgreSQL's behavior shown (pinned to PostgreSQL 17 docs, current revision).

| Level | Dirty read | Non-repeatable read | Phantom | Write skew / serialization anomaly |
|-------|-----------|---------------------|---------|------------------------------------|
| Read Committed (typical default) | No | Possible | Possible | Possible |
| Repeatable Read (PG: snapshot isolation) | No | No | No (in PG) | Possible |
| Serializable | No | No | No | No |

- **Read Committed**: each statement sees its own fresh snapshot. Cheapest, never aborts for serialization, but allows lost updates and write skew. Default in PostgreSQL and SQL Server.
- **Repeatable Read**: one snapshot for the whole transaction. Prevents non-repeatable/phantom reads but NOT write skew. In PostgreSQL it can abort with a serialization failure on concurrent update of a row this transaction read or wrote.
- **Serializable**: guarantees the result equals some serial order. Prevents write skew via predicate locking. Highest abort rate under contention.

Note: engines differ. MySQL/InnoDB defaults to Repeatable Read with different phantom behavior (gap locks); MySQL Serializable converts plain reads to locking reads. Confirm semantics against your engine's dated docs, not by analogy to PostgreSQL.

## Requirements

- **deliberate-level**: Each transaction MUST set its isolation level explicitly (e.g. `SET TRANSACTION ISOLATION LEVEL ...` or the driver/ORM equivalent) rather than relying on an unstated global default. The choice MUST be justified by the anomaly being prevented.
- **retry-serialization-failure**: Any transaction running at Repeatable Read or Serializable MUST be wrapped in retry logic that re-runs the whole transaction on a serialization failure. In PostgreSQL this is SQLSTATE `40001` (`could not serialize access due to ...`). MySQL/InnoDB raises deadlock (error `1213`/SQLSTATE `40001`) and lock-wait timeout (`1205`); treat both as retryable.
- **bounded-backoff**: Retries MUST be bounded (a fixed max attempt count, e.g. 3-5) with exponential backoff plus jitter. Code MUST NOT retry unboundedly; on exhaustion it MUST surface the failure.
- **idempotent-retry**: The retried transaction body MUST be safe to re-execute — no side effects (emails, payments, external calls, non-transactional counters) inside the retried block. See `agenticdevelopercookbook://principles/idempotency`.
- **no-savepoint-only-retry**: Retry MUST restart from a fresh `BEGIN`. Catching `40001` and continuing in the same aborted transaction is invalid — the transaction is already doomed.
- **explicit-locking-for-queues**: Worker/queue claim patterns MUST use explicit row locking — `SELECT ... FOR UPDATE SKIP LOCKED` to let concurrent workers grab disjoint rows, or `FOR UPDATE` (optionally `NOWAIT`) when blocking is acceptable. They SHOULD NOT rely on Serializable for queue dispatch (it serializes throughput).
- **prefer-narrowest-level**: Transactions SHOULD use the narrowest level that prevents the anomaly that actually matters. Reach for Serializable only when write skew is a real risk (e.g. invariant across multiple rows: "at least one admin", balance checks across accounts).

## Choosing a level

- Reads only, tolerant of slight staleness → **Read Committed**.
- Multi-statement report needing a consistent snapshot → **Repeatable Read**.
- Enforcing an invariant that spans rows the transaction reads then writes (write skew) → **Serializable**, with retry.

## Retry pattern (pseudocode)

```
for attempt in 1..MAX:                  # MAX bounded, e.g. 4
    try:
        begin(isolation = SERIALIZABLE)
        result = run_pure_transaction()  # no external side effects
        commit()
        return result
    except SerializationFailure as e:    # SQLSTATE 40001 (or InnoDB 1213/1205)
        rollback()
        if attempt == MAX: raise
        sleep(base * 2**attempt + jitter())
```

## Anti-patterns

- Treating `40001` as a hard error and surfacing it to the user — it is expected under contention and MUST be retried.
- Using Read Committed for a check-then-update invariant (read balance, then debit) — this loses updates; use `SELECT ... FOR UPDATE` or Serializable.
- Emitting side effects (charge a card, send a webhook) inside a Serializable transaction body that may be retried.

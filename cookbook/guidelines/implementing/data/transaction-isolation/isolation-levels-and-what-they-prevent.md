
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


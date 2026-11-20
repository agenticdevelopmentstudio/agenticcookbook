
- Reads only, tolerant of slight staleness → **Read Committed**.
- Multi-statement report needing a consistent snapshot → **Repeatable Read**.
- Enforcing an invariant that spans rows the transaction reads then writes (write skew) → **Serializable**, with retry.


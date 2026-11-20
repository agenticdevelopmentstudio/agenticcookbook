
- Because each step is additive and backward-compatible, the rollback is to **redeploy the previous app version** — the expanded schema still works for it. Avoid down-migrations that drop just-added columns during an incident; they re-introduce the lock you were avoiding.
- The old shape **MUST** survive at least one full deploy cycle past the switch so any in-flight N-1 instances stay functional.

> Note: exact lock behavior and which `ALTER TABLE` operations rewrite the table vary by database engine and version. The Postgres examples here are illustrative; confirm against your engine's current `ALTER TABLE` documentation before relying on a clause being non-blocking.


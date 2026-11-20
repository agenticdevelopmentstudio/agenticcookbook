
- Run the app's full transaction set against a transaction-mode pooler in staging; assert no `prepared statement does not exist` / `InvalidSqlStatementName` errors under concurrency.
- Grep the codebase for `SET ` (non-`LOCAL`), `LISTEN`, `pg_advisory_lock(` (non-`_xact_`), and session temp-table usage before deploying behind transaction pooling.


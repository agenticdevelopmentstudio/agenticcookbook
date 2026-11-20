
| Mode | Connection held for | Use when | Cost |
|------|--------------------|----------|------|
| Session | Whole client session | Need full session features | Lowest multiplexing; one server conn per active client |
| Transaction | One transaction | High fan-out, short transactions | Best multiplexing; breaks session-scoped state |
| Statement | One statement (autocommit only) | Extreme fan-out, no multi-statement txns | Most aggressive; disallows multi-statement transactions |

- **prefer-transaction-mode**: For high fan-out (serverless, many instances) the pooler **SHOULD** run in **transaction mode** (PgBouncer, Supavisor, or a managed equivalent). It returns the server connection to the pool at each `COMMIT`/`ROLLBACK`, so a few dozen server connections serve thousands of clients.
- **session-mode-fallback**: Use **session mode** only when the workload genuinely needs session-scoped features (below) and you accept near-1:1 client-to-server connection mapping.


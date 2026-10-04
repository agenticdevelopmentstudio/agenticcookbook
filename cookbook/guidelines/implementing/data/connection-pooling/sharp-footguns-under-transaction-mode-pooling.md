
Transaction mode reassigns the server connection between transactions, so any state scoped to a session — not a transaction — silently breaks. Code that runs under transaction-mode pooling **MUST NOT** depend on:

- **no-session-set**: Session-level `SET` / `RESET` of GUCs (e.g. `SET statement_timeout`, `SET search_path`, `SET ROLE`, time zone). Use the per-transaction form `SET LOCAL` inside an explicit transaction instead.
- **no-listen-notify**: `LISTEN` / `NOTIFY`. The notification channel is session-scoped; the listener will not reliably receive events. Use a dedicated session-mode connection or a separate message bus.
- **no-session-advisory-locks**: Session-level advisory locks (`pg_advisory_lock`). Use **transaction-scoped** advisory locks (`pg_advisory_xact_lock`) so the lock is bound to a transaction the pooler keeps intact.
- **no-temp-tables**: Session-scoped temporary tables and `WITH HOLD` cursors that outlive a transaction.
- **prepared-statements-caveat**: Server-side `PREPARE`/`DEALLOCATE` issued as SQL text. As a forecast-now-shipped nuance: PgBouncer added protocol-level prepared-statement support (1.21, 2023) enabled by default since 1.24 (January 2025), so protocol-prepared statements via the client library (e.g. libpq `PQprepare`) work in transaction mode. Verify your pooler version and that your driver uses the extended protocol, not text-mode `PREPARE`. Confirm against your deployed pooler's docs.


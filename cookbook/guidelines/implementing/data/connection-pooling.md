---
id: b8fa0cf0-b15b-4eec-a161-7fbd6936f1d9
title: "Connection pooling for server and serverless backends"
domain: agenticdevelopercookbook://guidelines/implementing/data/connection-pooling
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Front Postgres with a transaction-mode pooler for serverless or many-instance backends, and never depend on session-scoped state."
platforms: []
tags:
  - database
  - scaling
  - backend
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/data/transaction-isolation
references:
  - https://www.pgbouncer.org/
  - https://learn.microsoft.com/en-us/azure/postgresql/connectivity/concepts-connection-pooling-best-practices
  - https://www.pgbouncer.org/usage.html
  - https://devcenter.heroku.com/articles/best-practices-pgbouncer-configuration
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - database-operations
  - performance-optimization
---

# Connection pooling for server and serverless backends

Each PostgreSQL connection is a heavyweight, per-backend OS process (default `max_connections` is typically ~100). A connection pooler multiplexes many client connections onto a small set of server connections. A pooler is effectively mandatory once you run roughly 10+ application instances, and **MUST** be used for any serverless workload, where per-invocation connection churn would otherwise exhaust the server.

## When a pooler is required

- **serverless-pooler**: Serverless / autoscaling functions (Lambda, Cloud Run, Cloudflare Workers, Vercel) **MUST** connect through a pooler. Each cold start and concurrent invocation opens its own connection; without pooling you hit `FATAL: too many connections` under modest load.
- **many-instance-pooler**: Backends running ~10+ application instances or with large per-instance internal pools **SHOULD** front Postgres with a pooler rather than raising `max_connections`, which raises per-connection memory and contention.
- **single-instance-exception**: A single long-lived server with a bounded internal pool (e.g. one app process, `pool_size` < ~20) MAY connect directly without an external pooler.

## Pooling modes

| Mode | Connection held for | Use when | Cost |
|------|--------------------|----------|------|
| Session | Whole client session | Need full session features | Lowest multiplexing; one server conn per active client |
| Transaction | One transaction | High fan-out, short transactions | Best multiplexing; breaks session-scoped state |
| Statement | One statement (autocommit only) | Extreme fan-out, no multi-statement txns | Most aggressive; disallows multi-statement transactions |

- **prefer-transaction-mode**: For high fan-out (serverless, many instances) the pooler **SHOULD** run in **transaction mode** (PgBouncer, Supavisor, or a managed equivalent). It returns the server connection to the pool at each `COMMIT`/`ROLLBACK`, so a few dozen server connections serve thousands of clients.
- **session-mode-fallback**: Use **session mode** only when the workload genuinely needs session-scoped features (below) and you accept near-1:1 client-to-server connection mapping.

## Sharp footguns under transaction-mode pooling

Transaction mode reassigns the server connection between transactions, so any state scoped to a session — not a transaction — silently breaks. Code that runs under transaction-mode pooling **MUST NOT** depend on:

- **no-session-set**: Session-level `SET` / `RESET` of GUCs (e.g. `SET statement_timeout`, `SET search_path`, `SET ROLE`, time zone). Use the per-transaction form `SET LOCAL` inside an explicit transaction instead.
- **no-listen-notify**: `LISTEN` / `NOTIFY`. The notification channel is session-scoped; the listener will not reliably receive events. Use a dedicated session-mode connection or a separate message bus.
- **no-session-advisory-locks**: Session-level advisory locks (`pg_advisory_lock`). Use **transaction-scoped** advisory locks (`pg_advisory_xact_lock`) so the lock is bound to a transaction the pooler keeps intact.
- **no-temp-tables**: Session-scoped temporary tables and `WITH HOLD` cursors that outlive a transaction.
- **prepared-statements-caveat**: Server-side `PREPARE`/`DEALLOCATE` issued as SQL text. As a forecast-now-shipped nuance: PgBouncer added protocol-level prepared-statement support (1.21, 2023) enabled by default since 1.24 (January 2025), so protocol-prepared statements via the client library (e.g. libpq `PQprepare`) work in transaction mode. Verify your pooler version and that your driver uses the extended protocol, not text-mode `PREPARE`. Confirm against your deployed pooler's docs.

## Practical configuration

- **disable-driver-side-prepare**: When unsure of pooler support, configure the driver/ORM to avoid named server-side prepared statements (e.g. set query/plan caching off, or use a pooler-aware setting) and rely on `SET LOCAL` for per-request GUCs.
- **size-the-pool**: Set the pooler's server pool (`default_pool_size`) below `max_connections` with headroom for migrations, admin, and direct connections. Total server connections across all poolers **MUST** stay under `max_connections`.
- **separate-pool-for-session-work**: Migrations, `LISTEN`/`NOTIFY`, and admin tasks that need session features **SHOULD** use a separate connection string pointed at a session-mode pool or directly at Postgres.
- **fail-fast-on-exhaustion**: Configure short client-side connection acquisition timeouts so an exhausted pool surfaces a fast, observable error rather than hanging requests.

## Verify

- Run the app's full transaction set against a transaction-mode pooler in staging; assert no `prepared statement does not exist` / `InvalidSqlStatementName` errors under concurrency.
- Grep the codebase for `SET ` (non-`LOCAL`), `LISTEN`, `pg_advisory_lock(` (non-`_xact_`), and session temp-table usage before deploying behind transaction pooling.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |

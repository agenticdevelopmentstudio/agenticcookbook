
- **disable-driver-side-prepare**: When unsure of pooler support, configure the driver/ORM to avoid named server-side prepared statements (e.g. set query/plan caching off, or use a pooler-aware setting) and rely on `SET LOCAL` for per-request GUCs.
- **size-the-pool**: Set the pooler's server pool (`default_pool_size`) below `max_connections` with headroom for migrations, admin, and direct connections. Total server connections across all poolers **MUST** stay under `max_connections`.
- **separate-pool-for-session-work**: Migrations, `LISTEN`/`NOTIFY`, and admin tasks that need session features **SHOULD** use a separate connection string pointed at a session-mode pool or directly at Postgres.
- **fail-fast-on-exhaustion**: Configure short client-side connection acquisition timeouts so an exhausted pool surfaces a fast, observable error rather than hanging requests.


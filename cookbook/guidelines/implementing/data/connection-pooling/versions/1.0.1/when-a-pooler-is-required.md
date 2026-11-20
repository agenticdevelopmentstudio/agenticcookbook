
- **serverless-pooler**: Serverless / autoscaling functions (Lambda, Cloud Run, Cloudflare Workers, Vercel) **MUST** connect through a pooler. Each cold start and concurrent invocation opens its own connection; without pooling you hit `FATAL: too many connections` under modest load.
- **many-instance-pooler**: Backends running ~10+ application instances or with large per-instance internal pools **SHOULD** front Postgres with a pooler rather than raising `max_connections`, which raises per-connection memory and contention.
- **single-instance-exception**: A single long-lived server with a bounded internal pool (e.g. one app process, `pool_size` < ~20) MAY connect directly without an external pooler.



# Connection pooling for server and serverless backends

Each PostgreSQL connection is a heavyweight, per-backend OS process (default `max_connections` is typically ~100). A connection pooler multiplexes many client connections onto a small set of server connections. A pooler is effectively mandatory once you run roughly 10+ application instances, and **MUST** be used for any serverless workload, where per-invocation connection churn would otherwise exhaust the server.


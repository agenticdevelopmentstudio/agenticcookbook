
Postgres-to-SQLite sync engine with a server-authoritative write path.

**Architecture:** PowerSync Service connects to Postgres via logical replication (read-only) and streams data to client SQLite based on configurable Sync Rules. Client writes queue locally, then go through your own backend — your backend applies business logic, validation, and authorization before committing to Postgres. Changes committed to Postgres flow back to all clients via PowerSync.

**Key differentiator:** You control the write path. The server can reject, transform, or merge client writes with custom logic.

**Sync Rules** enable dynamic partial replication (e.g., sync only tasks belonging to the current user):

```yaml
- table: tasks
  filter: "user_id = token_parameters.user_id"
```

**Supported backends:** PostgreSQL (GA), MongoDB (GA).

**Use when:** You need server-authoritative writes with custom business logic, per-user data partitioning, and production-grade reliability.


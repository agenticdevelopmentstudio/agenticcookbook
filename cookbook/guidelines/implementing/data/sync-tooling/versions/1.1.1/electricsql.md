
Syncs PostgreSQL with client-side SQLite using Postgres logical replication (WAL streaming).

**Architecture:** An Electric service reads the Postgres WAL and streams changes to client-side SQLite (browser via WASM, mobile via native SQLite). Client writes go through Electric back to Postgres. Conflict resolution uses CRDTs (LWW semantics per field).

**Key characteristic:** "Direct-to-Postgres" — writes bypass your application backend. Validation happens via Postgres constraints and DDLX rules only.

**Trade-offs:**
- Pro: No backend code needed for sync
- Con: Cannot inject custom business logic on the write path
- Con: Requires SUPERUSER database privileges; modifies Postgres schema with shadow tables and triggers

**Use when:** The write path needs no custom logic, and you can accept Postgres-only as the server database.



# Transaction isolation and serialization-failure retry

Multi-writer databases (PostgreSQL, MySQL/InnoDB, SQL Server, CockroachDB) use snapshot-based concurrency where transactions can conflict at commit time. Unlike SQLite's single-writer model, code MUST choose an isolation level deliberately and retry the serialization failures that stronger levels can raise.


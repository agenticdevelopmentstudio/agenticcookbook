
Streaming WAL-based replication for disaster recovery. NOT a multi-device sync tool.

Litestream takes over SQLite's WAL checkpointing, continuously streams new WAL pages to cloud storage (S3, Azure Blob, SFTP, GCS), and can create read replicas on other servers.

**Use when:** You need server-side SQLite backup, point-in-time recovery, or read replicas for a single-writer SQLite deployment. Do not use for device-to-server sync or multi-writer scenarios.


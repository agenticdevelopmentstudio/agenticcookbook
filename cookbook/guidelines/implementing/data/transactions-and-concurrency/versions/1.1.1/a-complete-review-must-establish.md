
- WAL mode enabled (PRAGMA journal_mode = WAL)
- Write transactions use BEGIN IMMEDIATE; read transactions use BEGIN DEFERRED
- busy_timeout set to reasonable value (e.g., 5000ms) to prevent SQLITE_BUSY errors
- Production PRAGMAs configured: synchronous=NORMAL, cache_size=-64000, journal_size_limit, foreign_keys=ON
- Connection pooling implements single-writer pattern for write transactions
- Transaction isolation levels understood and documented for concurrent read scenarios

A review passes when it establishes every item above.

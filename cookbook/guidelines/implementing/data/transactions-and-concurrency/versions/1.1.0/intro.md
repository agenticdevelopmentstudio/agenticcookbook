
# Transactions and Concurrency

Transaction management is the single most impactful performance lever in SQLite. Individual autocommit inserts each pay a full fsync — wrapping them in explicit transactions reduces that cost to one fsync per batch. WAL mode unlocks concurrent reads alongside writes and cuts per-commit overhead from 30ms+ to under 1ms.


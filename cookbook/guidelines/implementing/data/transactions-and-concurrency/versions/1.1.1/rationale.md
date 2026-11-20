
- `must-wrap-write-batches-in-transactions`: Even a modest batch (10–100 rows) benefits significantly.
- `must-use-begin-immediate-for-writes`: It fails fast at `BEGIN` time rather than mid-transaction after work has been done.
- `must-set-busy-timeout`: A value of 5000ms (5 seconds) is a safe default.
- `should-set-wal-on-connection-open`: WAL mode persists in the database header, so it need only be set once per database, but re-setting it on connection open is safe and recommended.
- `should-not-disable-auto-checkpoint-without-replacement`, `should-not-hold-long-read-transactions`, `should-not-run-very-large-write-transactions`: These are the three causes of WAL growth to avoid: each one keeps the checkpoint from resetting the WAL, so the WAL file grows without bound.


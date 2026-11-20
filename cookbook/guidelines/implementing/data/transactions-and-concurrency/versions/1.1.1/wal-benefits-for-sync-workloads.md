
Sync operations write in bursts (a batch of changes arrives, gets applied, then the connection idles). WAL mode is well-suited to this pattern:

- Readers continue to serve UI queries while the sync write transaction runs
- Sequential WAL appends are faster than random writes into the main database file
- `BEGIN IMMEDIATE` on the sync writer prevents mid-batch lock failures
- After a large batch, a `TRUNCATE` checkpoint resets WAL size without blocking readers for long

For concurrent sync read/write access, WAL mode with a single write connection and a `busy_timeout` of 5,000ms eliminates nearly all `SQLITE_BUSY` errors in practice.


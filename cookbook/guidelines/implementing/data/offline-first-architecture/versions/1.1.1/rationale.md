
- `must-enable-wal-for-synced-databases`: WAL mode enables concurrent readers and writers: readers never block writers, writers never block readers. This is essential for offline-first apps where the sync worker writes in the background while the UI reads. With the default rollback journal, a background write locks the entire database and freezes the UI.
- `must-write-mutation-and-outbox-atomically`: This guarantees that whatever is visible on screen is queued for sync.
- `must-read-ui-from-local-sqlite`: Changes appear instantly after the local write — the user does not wait for the server.
- `must-roll-back-on-server-rejection`: Silently ignoring rejections causes local and server state to diverge permanently.
- `must-run-migrations-regardless-of-network`: Devices may be offline when a new app version with schema changes ships.
- `should-prune-sync-metadata-on-schedule`: Local SQLite databases grow unbounded without maintenance. Sync metadata — outbox entries, change logs, tombstones — accumulates fastest.


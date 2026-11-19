
Before applying any migration or schema change to a production database:

1. **Back up the database** — use `.backup`, `VACUUM INTO`, or the Online Backup API. For production server-side SQLite with Litestream, verify the continuous backup is current and a snapshot exists.
2. **Verify the backup is restorable** — restore to a temporary location and run `PRAGMA quick_check`. A backup that cannot be restored is not a backup.
3. **Record the current schema version** — `PRAGMA user_version` or equivalent. This is your rollback target if the migration fails.


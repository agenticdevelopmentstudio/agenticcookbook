<!-- leaf: ship-general/backup-and-recovery · source: guidelines/shipping/backup-and-recovery.md -->

**Rules** (cite as `ship-general/backup-and-recovery#<slug>`):

- `restoring-backup-you-delete-existing-wal-shm` MUST — When restoring a backup, you MUST delete any existing *-wal and *-shm files at the destination before copying the …

# Database backup and recovery

Before shipping any database change — migration, schema update, or data transformation — verify that backup and recovery procedures are in place and tested.

## Pre-deploy backup checklist

Before applying any migration or schema change to a production database:

1. **Back up the database** — use `.backup`, `VACUUM INTO`, or the Online Backup API. For production server-side SQLite with Litestream, verify the continuous backup is current and a snapshot exists.
2. **Verify the backup is restorable** — restore to a temporary location and run `PRAGMA quick_check`. A backup that cannot be restored is not a backup.
3. **Record the current schema version** — `PRAGMA user_version` or equivalent. This is your rollback target if the migration fails.

## WAL files during restore

When restoring a backup, you MUST delete any existing `*-wal` and `*-shm` files at the destination before copying the backup file. A stale or mismatched WAL file will corrupt the restored database.

```bash
rm -f restored.db-wal restored.db-shm
cp backup.db restored.db
```

## Pre-deploy integrity check

Run `PRAGMA quick_check` on the production database before applying migrations. If the database is already damaged, applying a migration will make recovery harder. `integrity_check` is more thorough but slower — use it for scheduled audits, not deploy gates.

## Post-deploy verification

After a migration completes:

1. Run `PRAGMA quick_check` to confirm the database is intact
2. Run `PRAGMA foreign_key_check` if the migration touched foreign key relationships
3. Verify the schema version was incremented correctly

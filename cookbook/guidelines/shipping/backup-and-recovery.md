---
id: 04b47c8b-e076-47a0-a541-6937bdc64abb
title: "Database backup and recovery"
domain: agenticdevelopercookbook://guidelines/shipping/backup-and-recovery
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-04-06
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pre-deployment backup verification: ensure backups run before migrations, WAL files are handled during restore, and integrity checks pass before shipping."
platforms:
  - sqlite
  - postgresql
tags:
  - database
  - backup
  - recovery
  - operations
  - litestream
  - wal
depends-on: []
related:
  - guidelines/data/sqlite-best-practices.md
references:
  - https://sqlite.org/backup.html
  - https://sqlite.org/howtocorrupt.html
  - https://sqlite.org/recovery.html
  - https://litestream.io/how-it-works/
  - https://sqlite.org/wal.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-06"
triggers:
  - database-operations
  - configuration
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for shipping use case — focus on pre-deploy backup verification |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-04-06 | Mike Fullerton | Initial version |

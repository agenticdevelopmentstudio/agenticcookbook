<!-- leaf: ship-general/schema-evolution · source: guidelines/shipping/schema-evolution.md -->

**Rules** (cite as `ship-general/schema-evolution#<slug>`):

- `version-tracking` MUST — every migration MUST increment PRAGMA user_version (or the schema_migrations table for sync contexts). Verify the …
- `transaction-wrapping` MUST — each migration MUST be wrapped in a transaction. A failed migration must leave the database unchanged.
- `idempotency` MUST — every migration MUST be safe to run twice. Verify with a dry-run against a backup.
- `backup-exists` MUST — a verified, restorable backup MUST exist before applying the migration (see backup-and-recovery guideline).
- `step-recreate-procedure-tested-against-production-equivalent` MUST — Breaking changes require the 12-step recreate procedure and MUST be tested against production-equivalent data before …
- `migration-have-documented-rollback-path` MUST — Every migration MUST have a documented rollback path before shipping:
- `reverse-migration-script-exist-tested` MUST — For destructive changes (column removal, type changes): a reverse migration script MUST exist and be tested

# Schema evolution and migrations

Before shipping any schema change, verify the migration is tracked, idempotent, backward-compatible, and has a rollback path.

## Pre-deploy migration checklist

1. **Version tracking** — every migration MUST increment `PRAGMA user_version` (or the `schema_migrations` table for sync contexts). Verify the version number is correct and sequential.
2. **Transaction wrapping** — each migration MUST be wrapped in a transaction. A failed migration must leave the database unchanged.
3. **Idempotency** — every migration MUST be safe to run twice. Verify with a dry-run against a backup.
4. **Backup exists** — a verified, restorable backup MUST exist before applying the migration (see backup-and-recovery guideline).

## Backward compatibility check

Before shipping, verify the migration is backward-compatible:

- **Safe changes** (can ship without coordination): adding a nullable column, adding a column with a DEFAULT, creating a new index, renaming a column.
- **Breaking changes** (require migration coordination): changing column types, removing columns, adding NOT NULL constraints without defaults, dropping tables.

Breaking changes require the 12-step recreate procedure and MUST be tested against production-equivalent data before shipping. See the implementing copy of this guideline for the procedure.

## Sync compatibility verification

For sync-capable schemas, verify before shipping:

1. A device on the old schema can still sync with the server on the new schema
2. New columns have DEFAULT values (CRDTs require values for all rows)
3. Migrations have been tested against databases at every previous version — an offline device may skip versions
4. Server-side backup exists before applying

## Rollback strategy

Every migration MUST have a documented rollback path before shipping:

- For additive changes (new columns, new indexes): rollback is optional — the old code ignores new columns
- For destructive changes (column removal, type changes): a reverse migration script MUST exist and be tested
- Record the pre-migration `user_version` as the rollback target

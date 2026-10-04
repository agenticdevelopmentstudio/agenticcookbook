---
id: a5228bfe-3caa-444b-9952-52ca5244f829
title: "Schema evolution and migrations"
domain: agenticdevelopercookbook://guidelines/shipping/schema-evolution
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-04-06
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pre-deploy migration verification: ensure version tracking, idempotency, sync compatibility, and rollback strategy before shipping schema changes."
platforms:
  - sqlite
  - postgresql
tags:
  - database
  - migrations
  - schema-evolution
  - schema-design
  - sync
depends-on: []
related:
  - guidelines/data/sqlite-best-practices.md
references:
  - https://sqlite.org/lang_altertable.html
  - https://david.rothlis.net/declarative-schema-migration-for-sqlite/
  - https://levlaz.org/sqlite-db-migrations-with-pragma-user_version/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-06"
triggers:
  - database-operations
  - schema-design
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for shipping use case — focus on pre-deploy verification and rollback |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-04-06 | Mike Fullerton | Initial version |

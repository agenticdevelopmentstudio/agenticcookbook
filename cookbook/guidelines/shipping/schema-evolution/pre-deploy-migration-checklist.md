
1. **Version tracking** — every migration MUST increment `PRAGMA user_version` (or the `schema_migrations` table for sync contexts). Verify the version number is correct and sequential.
2. **Transaction wrapping** — each migration MUST be wrapped in a transaction. A failed migration must leave the database unchanged.
3. **Idempotency** — every migration MUST be safe to run twice. Verify with a dry-run against a backup.
4. **Backup exists** — a verified, restorable backup MUST exist before applying the migration (see backup-and-recovery guideline).



Every migration MUST have a documented rollback path before shipping:

- For additive changes (new columns, new indexes): rollback is optional — the old code ignores new columns
- For destructive changes (column removal, type changes): a reverse migration script MUST exist and be tested
- Record the pre-migration `user_version` as the rollback target


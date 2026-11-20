
# Schema evolution and migrations

Version every SQLite schema with `PRAGMA user_version` and evolve it through ordered, tested migrations that respect ALTER TABLE's limits and stay sync-compatible.

Before shipping any schema change, verify the migration is tracked, idempotent, backward-compatible, and has a rollback path.

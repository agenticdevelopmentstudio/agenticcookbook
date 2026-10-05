
# Schema evolution and migrations

Version every SQLite schema with `PRAGMA user_version` and evolve it through ordered, tested migrations that respect ALTER TABLE's limits and stay sync-compatible.


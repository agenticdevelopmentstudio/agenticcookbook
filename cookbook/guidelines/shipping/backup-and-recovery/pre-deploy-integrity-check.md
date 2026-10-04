
Run `PRAGMA quick_check` on the production database before applying migrations. If the database is already damaged, applying a migration will make recovery harder. `integrity_check` is more thorough but slower — use it for scheduled audits, not deploy gates.


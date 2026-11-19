
After a migration completes:

1. Run `PRAGMA quick_check` to confirm the database is intact
2. Run `PRAGMA foreign_key_check` if the migration touched foreign key relationships
3. Verify the schema version was incremented correctly


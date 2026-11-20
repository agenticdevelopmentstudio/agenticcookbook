
SQLite 3.29.0+ includes a built-in recovery tool that extracts whatever data remains readable from a corrupted file.

```bash
sqlite3 corrupted.db ".recover" | sqlite3 recovered.db
```

For older versions, extract data manually:

```bash
sqlite3 corrupted.db ".mode insert" ".output dump.sql" ".dump" ".output stdout"
sqlite3 new.db < dump.sql
```

Recovery is always partial — some rows may be unrecoverable. The best recovery strategy is a recent backup.


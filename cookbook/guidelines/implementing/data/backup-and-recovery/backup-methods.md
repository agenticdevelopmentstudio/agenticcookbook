
Choose the backup method that matches your durability requirements and operational constraints.

**`.backup` command** is the recommended default for most cases. It performs a page-by-page replica without locking the database for the duration — other connections can continue writing, though their changes will not appear in the backup.

```bash
sqlite3 mydb.db ".backup backup.db"
```

**`VACUUM INTO`** produces a compacted copy and is preferred when storage efficiency matters. It is more CPU-intensive than `.backup` but eliminates free-page waste and defragments the file.

```sql
VACUUM INTO '/path/to/backup.db';
```

**Online Backup API** (programmatic) copies pages incrementally, acquiring a read lock only during each step rather than the entire backup. Use this when you need progress monitoring or integration into application code.

```python
source = sqlite3.connect('mydb.db')
dest   = sqlite3.connect('backup.db')
source.backup(dest, pages=100)   # copies 100 pages per step
dest.close()
source.close()
```

**Litestream** MUST be used when you need continuous, point-in-time recovery for a production server-side SQLite database. It takes over WAL checkpointing, streams WAL pages to S3-compatible storage, and periodically snapshots the full database.

```yaml
dbs:
  - path: /path/to/app.db
    replicas:
      - type: s3
        bucket: my-backup-bucket
        path: app.db
        retention: 72h
```

Litestream is a disaster-recovery tool, not a sync tool. It replicates one database to one storage destination. Do not use it to synchronize multiple writers.


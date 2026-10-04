
When restoring a backup, you MUST delete any existing `*-wal` and `*-shm` files at the destination before copying the backup file. A stale or mismatched WAL file will corrupt the restored database. The WAL and database file are a matched pair — they cannot be mixed.

```bash
rm -f restored.db-wal restored.db-shm
cp backup.db restored.db
```


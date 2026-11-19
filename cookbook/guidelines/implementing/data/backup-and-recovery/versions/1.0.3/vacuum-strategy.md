
Free pages accumulate as rows are deleted. SQLite does not return this space to the filesystem automatically.

**Prefer incremental VACUUM** for running applications. It reclaims a bounded number of pages per call without locking the database for long.

```sql
PRAGMA incremental_vacuum(500);  -- reclaim up to 500 pages
```

This requires `PRAGMA auto_vacuum = INCREMENTAL` set when the database was created.

**Full VACUUM** is appropriate after bulk deletes (25%+ of content removed) or offline maintenance windows. It rewrites the entire database and requires approximately 2x the database size in free disk space. It locks the database for its entire duration.

```sql
VACUUM;
```

SHOULD run VACUUM during application idle time (scheduled maintenance, app launch before first query). MUST NOT run VACUUM under high write load.


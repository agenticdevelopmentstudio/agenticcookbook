
The most recent modification wins. Implement on the server with an UPSERT that compares timestamps or version numbers:

```sql
INSERT INTO tasks (id, title, status, updated_at, version)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT (id) DO UPDATE SET
    title      = EXCLUDED.title,
    status     = EXCLUDED.status,
    updated_at = EXCLUDED.updated_at,
    version    = EXCLUDED.version
WHERE EXCLUDED.updated_at > tasks.updated_at;
```

SHOULD use Hybrid Logical Clock (HLC) timestamps rather than wall-clock time to avoid clock-skew errors. Physical clocks on different devices can diverge by seconds or more, causing the wrong write to win.

MUST NOT use LWW for collaborative editing, financial records, or inventory — silent overwrites are destructive in those domains.


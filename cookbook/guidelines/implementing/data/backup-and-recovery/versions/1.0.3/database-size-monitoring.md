
Monitor database size so you can detect unexpected growth and decide when to VACUUM.

```sql
SELECT page_count * page_size AS total_bytes,
       freelist_count * page_size AS free_bytes
FROM pragma_page_count(), pragma_page_size(), pragma_freelist_count();
```

Alert when `free_bytes / total_bytes` exceeds 25% — that is a signal to VACUUM.



```sql
SELECT page_count * page_size AS total_bytes,
       freelist_count * page_size AS free_bytes
FROM pragma_page_count(), pragma_page_size(), pragma_freelist_count();
```


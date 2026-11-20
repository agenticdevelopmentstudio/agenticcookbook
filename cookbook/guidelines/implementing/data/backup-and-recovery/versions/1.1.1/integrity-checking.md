
```sql
PRAGMA integrity_check;   -- thorough; slow on large databases
PRAGMA quick_check;       -- faster, catches most problems
```

`integrity_check` returns `ok` on a healthy database. Any other output indicates damage.


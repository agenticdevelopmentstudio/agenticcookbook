
Run integrity checks on a schedule or after any suspect event (disk errors, process kills, power loss).

```sql
PRAGMA integrity_check;   -- thorough; slow on large databases
PRAGMA quick_check;       -- faster, catches most problems
```

`integrity_check` returns `ok` on a healthy database. Any other output indicates damage. Schedule `quick_check` on startup for databases that are critical to the application. Reserve `integrity_check` for periodic offline audits.


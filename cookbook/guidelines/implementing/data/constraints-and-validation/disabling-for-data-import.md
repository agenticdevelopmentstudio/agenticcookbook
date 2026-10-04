
When importing potentially dirty data:

```sql
PRAGMA ignore_check_constraints = ON;
-- Import data...
PRAGMA ignore_check_constraints = OFF;
```

After import, verify integrity:

```sql
PRAGMA integrity_check;
```


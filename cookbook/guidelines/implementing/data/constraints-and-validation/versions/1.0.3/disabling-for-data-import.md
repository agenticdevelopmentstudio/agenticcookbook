
When importing potentially dirty data, a script MAY turn CHECK enforcement off:

```sql
PRAGMA ignore_check_constraints = ON;
-- Import data...
PRAGMA ignore_check_constraints = OFF;
```

After import, the script MUST verify integrity:

```sql
PRAGMA integrity_check;
```


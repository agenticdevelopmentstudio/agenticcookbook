
MUST be prefixed with `is_` or `has_`:

```sql
is_active    INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
has_children INTEGER NOT NULL DEFAULT 0 CHECK (has_children IN (0, 1))
```


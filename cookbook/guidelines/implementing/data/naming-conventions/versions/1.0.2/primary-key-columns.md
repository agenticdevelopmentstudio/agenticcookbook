
MUST use `<table_name>_id`, not bare `id`. Self-documenting PKs make JOIN bugs immediately visible:

```sql
-- Correct: mismatch is obvious
SELECT * FROM audit_log al
JOIN actors a ON a.actor_id = al.changed_by_actor_id;

-- Wrong: mismatches are invisible
SELECT * FROM audit_log al
JOIN actors a ON a.id = al.changed_by;
```


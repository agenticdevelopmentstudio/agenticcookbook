
When syncing SQLite with a server database, denormalized columns add sync complexity. Each write to the source data must also propagate to denormalized copies.

```sql
-- Trigger to maintain denormalized display_name on actors when humans table changes
CREATE TRIGGER tr_humans_after_update_display_name
AFTER UPDATE OF name ON humans
BEGIN
    UPDATE actors
    SET display_name = NEW.name
    WHERE actor_id = NEW.actor_id;
END;
```


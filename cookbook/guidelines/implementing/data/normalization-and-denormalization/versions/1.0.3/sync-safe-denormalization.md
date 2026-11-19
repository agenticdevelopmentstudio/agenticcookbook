
When syncing SQLite with a server database, denormalized columns add sync complexity. Each write to the source data must also propagate to denormalized copies.

Rules for denormalization in sync-capable schemas:
- MUST maintain the denormalized column via trigger so it stays in sync within the local database
- MUST include the denormalized column in sync payloads so the server stays consistent
- SHOULD treat the authoritative value as the normalized source; the denormalized copy is derived
- Prefer denormalizing immutable or rarely-changing data (names, labels) over frequently-changing values

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



ALL identifiers MUST use `snake_case`. SQL is case-insensitive for identifiers, so `CamelCase` creates false visual distinctions (`UnderValue` and `Undervalue` are identical to the engine). Underscores are unambiguous, readable across tools, and work well for non-native English speakers.

```sql
-- Correct
CREATE TABLE workflow_run (
    workflow_run_id  INTEGER PRIMARY KEY,
    workflow_name    TEXT NOT NULL,
    creation_date    TEXT NOT NULL DEFAULT (datetime('now')),
    is_active        INTEGER NOT NULL DEFAULT 1
);

-- Wrong
CREATE TABLE WorkflowRun (WorkflowRunID INTEGER PRIMARY KEY, ...);
```


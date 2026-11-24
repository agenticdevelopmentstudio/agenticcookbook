
This section is informative; its records are illustrations, not templates the guideline requires.

A superseded record, marked under its heading:

```markdown
# 7. Keep session data in the database

Status: superseded by [12. Keep session data in a shared cache](0012-session-cache.md)
Date: 2026-03-02
```

The record that replaces it:

```markdown
# 12. Keep session data in a shared cache

Status: accepted
Date: 2026-11-10
Decision-makers: platform team lead
Supersedes: [7. Keep session data in the database](0007-session-database.md)

## Context
Session reads now dominate database load at peak traffic.

## Considered options
- Shared cache: chosen; adds an operated component.
- Database with read replicas: rejected; replication lag breaks read-after-write for sessions.

## Decision
Session data moves to a shared cache.

## Consequences
- Good: database load at peak falls.
- Bad: the team now runs and monitors a cache cluster.
```

A Y-statement of the same decision: "In the context of the web shop service, facing the need to keep user session data consistent and current across instances, we decided for a shared cache and against database replicas, to achieve read-after-write consistency, accepting that the team operates one more component."



| Situation | Recommendation |
|-----------|---------------|
| New schema, unknown access patterns | Start at 3NF |
| Read-heavy dashboard, measured join bottleneck | Denormalize the join |
| Audit log display_name | Denormalize onto supertype table |
| Synced table with denormalized column | Maintain via trigger; include in sync payload |
| Count or sum of child rows | Do not store; query the child table |


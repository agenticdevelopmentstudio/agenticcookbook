
| Pattern | Read performance | Write complexity | Storage | Best for |
|---------|-----------------|-----------------|---------|----------|
| Adjacency list | Moderate (recursive) | Simple | Minimal | Dynamic trees with occasional depth queries |
| Closure table | Excellent | Moderate | High | Read-heavy, deep hierarchies |
| Nested sets | Excellent | High (renumbering) | Low | Static / rarely-modified hierarchies |

**Closure table** stores every ancestor-descendant path as a row, enabling efficient non-recursive queries:

```sql
CREATE TABLE category_closure (
    ancestor_id   INTEGER NOT NULL REFERENCES categories(category_id),
    descendant_id INTEGER NOT NULL REFERENCES categories(category_id),
    depth         INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (ancestor_id, descendant_id)
);

-- All descendants of node 1:
SELECT descendant_id FROM category_closure WHERE ancestor_id = 1;

-- Direct children only:
SELECT descendant_id FROM category_closure WHERE ancestor_id = 1 AND depth = 1;
```

Tradeoff: O(n²) worst-case storage and complex insert/delete maintenance.

**Nested sets** encode hierarchy as left/right boundary integers. Excellent read performance but inserting or moving a node requires renumbering all boundaries — impractical for frequently-modified trees.

**Start with adjacency list.** Migrate to closure table only if recursive queries become a measured performance problem.


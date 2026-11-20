
For hierarchical data, the simplest approach is a `parent_id` FK referencing the same table:

```sql
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    parent_id   INTEGER REFERENCES categories(category_id)  -- NULL = root
);
CREATE INDEX ix_categories_parent_id ON categories(parent_id);
```

Finding immediate children: `WHERE parent_id = ?`. Finding all descendants requires a recursive CTE (SQLite 3.8.3+):

```sql
WITH RECURSIVE descendants AS (
    SELECT category_id, name, parent_id FROM categories WHERE category_id = ?
    UNION ALL
    SELECT c.category_id, c.name, c.parent_id
    FROM categories c
    JOIN descendants d ON c.parent_id = d.category_id
)
SELECT * FROM descendants;
```


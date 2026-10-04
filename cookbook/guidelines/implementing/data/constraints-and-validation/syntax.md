
```sql
-- Column-level
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    quantity   INTEGER NOT NULL CHECK (quantity >= 0),
    price      REAL NOT NULL CHECK (price > 0)
);

-- Table-level (can reference multiple columns)
CREATE TABLE events (
    event_id   INTEGER PRIMARY KEY,
    start_date TEXT NOT NULL,
    end_date   TEXT NOT NULL,
    CHECK (end_date >= start_date)
);

-- Named constraint (recommended for large schemas)
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    salary      REAL NOT NULL,
    CONSTRAINT ck_employees_salary CHECK (salary > 0)
);
```

There is no functional difference between column-level and table-level CHECK constraints. Use table-level only when the expression references multiple columns.


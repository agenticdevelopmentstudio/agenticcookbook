
**Enum-like (restricted values):**

```sql
status    TEXT NOT NULL CHECK (status IN ('pending', 'active', 'completed', 'failed')),
priority  INTEGER NOT NULL CHECK (priority IN (1, 2, 3, 4, 5)),
direction TEXT NOT NULL CHECK (direction IN ('inbound', 'outbound'))
```

**Boolean enforcement:**

```sql
is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
```

**Range validation:**

```sql
age     INTEGER NOT NULL CHECK (age >= 0 AND age <= 150),
score   REAL NOT NULL CHECK (score BETWEEN 0.0 AND 100.0),
percent INTEGER NOT NULL CHECK (percent >= 0 AND percent <= 100)
```

**Pattern matching:**

```sql
email TEXT NOT NULL CHECK (email LIKE '%_@_%.__%'),
phone TEXT CHECK (phone LIKE '+%' OR phone IS NULL),
code  TEXT NOT NULL CHECK (
    length(code) = 6 AND code GLOB '[A-Z][A-Z][0-9][0-9][0-9][0-9]'
)
```

**String length:**

```sql
username TEXT NOT NULL CHECK (length(username) >= 3 AND length(username) <= 50),
api_key  TEXT NOT NULL CHECK (length(api_key) = 32)
```

**Multi-column constraint:**

```sql
CHECK (end_date > start_date),
CHECK (discount > 0 AND discount <= 1.0)
```

**Conditional logic:**

```sql
CHECK (
    (status = 'surplus' AND stock >= 500) OR
    (status != 'surplus')
)
```



- `must-store-dates-as-iso-8601-text`: It sorts correctly lexicographically.
- `must-use-text-for-strings`: `STRING` does NOT give TEXT affinity. Rule 5 (NUMERIC) applies because "STRING" contains neither "CHAR", "CLOB", nor "TEXT". This causes silent data corruption.
- `must-not-use-strict-below-3-37-0`: Databases with STRICT tables cannot be opened by SQLite before 3.37.0.


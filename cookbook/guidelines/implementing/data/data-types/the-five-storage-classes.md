
Every value belongs to exactly one storage class:

| Storage Class | Description |
|---------------|-------------|
| `NULL` | Null value |
| `INTEGER` | Signed integer (1–8 bytes, variable) |
| `REAL` | IEEE 754 float (8 bytes) |
| `TEXT` | UTF-8 string |
| `BLOB` | Raw bytes |

There is no `BOOLEAN`, `DATE`, or `DATETIME` type. These must be represented as `INTEGER` or `TEXT`.


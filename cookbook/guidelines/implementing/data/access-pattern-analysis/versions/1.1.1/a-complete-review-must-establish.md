
- All hot-path queries identified and mapped to available indexes
- Every WHERE, JOIN, and ORDER BY column has index coverage or explicitly chosen denormalization justifies lack of index
- Read/write ratio documented; schema normalized for high-write or denormalized for high-read as appropriate
- Batch sizes specified for sync operations (e.g., pull 1000 rows per batch, push 500 rows per transaction)
- Access patterns documented in code comments or design documentation for future maintainers

A review passes when it establishes every item above.

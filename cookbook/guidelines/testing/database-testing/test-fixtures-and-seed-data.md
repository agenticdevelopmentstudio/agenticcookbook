
SHOULD maintain a `test_seeds.sql` file with representative fixture data. Seed data SHOULD cover:

- Typical records (normal state)
- Edge cases (nulls, empty strings, boundary values)
- Records in each relevant status (e.g., pending, active, deleted)

MUST NOT build fixture data record-by-record inside individual tests when the same data is needed across multiple tests. Shared seed files are easier to maintain and faster to apply.

Use function-scoped fixtures for tests that write. Use session-scoped fixtures for read-only tests.



- Any operation that issues **more than one statement and must be atomic** (read-modify-write, multi-table insert, batch upsert with dependent rows) **MUST** be wrapped in a single transaction — annotate the DAO method with `@Transaction`, or call `db.withTransaction { ... }` from suspend code.
- `@Transaction` is also **REQUIRED** on `@Query` methods that return a `@Relation`-bearing POJO, so the parent and child reads see a consistent snapshot.
- Keep transactions short; do no network or long CPU work inside `withTransaction`. See `agenticdevelopercookbook://guidelines/implementing/data/transaction-isolation` for isolation semantics.


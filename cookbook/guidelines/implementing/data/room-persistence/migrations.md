
- On every schema change you **MUST** bump the database `version` and supply a `Migration` (or an `@DeleteColumn`/`@RenameColumn`-driven auto-migration spec). You **MUST NOT** ship `fallbackToDestructiveMigration()` in a release build — it silently drops user data.
- You **SHOULD** add a `MigrationTestHelper`-based instrumented test that opens the exported schema at version N and migrates to N+1, asserting data survives.


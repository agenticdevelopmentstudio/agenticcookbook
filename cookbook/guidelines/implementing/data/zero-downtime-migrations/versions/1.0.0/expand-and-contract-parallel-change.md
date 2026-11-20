
Spread one logical change across multiple releases:

| Phase | Action | Compatibility |
|-------|--------|---------------|
| **Expand** | Add new column/table/index. Make it nullable or defaulted. | Old code ignores it; new code may use it |
| **Migrate** | Dual-write (app writes old + new) and backfill existing rows in batches | Reads still served from old shape |
| **Switch** | Move reads to the new shape once backfill is complete and verified | New code reads new; old code still reads old |
| **Contract** | Stop dual-writing, drop the old column/table/index | Only run after no deployed version uses the old shape |

- New columns **MUST** be added as nullable or with a safe default; do not add `NOT NULL` to an existing large table in one step. Add the column, backfill, then add the constraint as `NOT VALID` and `VALIDATE CONSTRAINT` separately.
- Renames **MUST** be done as add-new + dual-write + backfill + switch + drop-old, never as an in-place `RENAME` that breaks N-1.
- Backfills **MUST** run in bounded batches (e.g. by primary-key range) with a commit per batch, so they hold no long transaction and can resume after interruption.
- Backfill jobs **SHOULD** be idempotent so a re-run after partial failure produces the same result.


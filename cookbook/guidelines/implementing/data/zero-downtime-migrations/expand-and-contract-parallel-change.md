
| Phase | Action | Compatibility |
|-------|--------|---------------|
| **Expand** | Add new column/table/index. Make it nullable or defaulted. | Old code ignores it; new code may use it |
| **Migrate** | Dual-write (app writes old + new) and backfill existing rows in batches | Reads still served from old shape |
| **Switch** | Move reads to the new shape once backfill is complete and verified | New code reads new; old code still reads old |
| **Contract** | Stop dual-writing, drop the old column/table/index | Only run after no deployed version uses the old shape |

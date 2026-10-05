
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| rop-001 | audit-inventory-all-rules | `.claude/rules/` with 3 files (50, 100, 200 lines) | Inventory lists all 3 with correct line/byte counts |
| rop-002 | audit-measure-per-turn-cost | 2 ungated rules (100 lines each), 1 globs-scoped rule (50 lines) | Per-turn cost = 200 lines (only ungated rules counted) |
| rop-003 | audit-detect-duplication | 2 rules with identical "Do not skip testing" paragraph | Finding identifies the duplicate with both file paths and matching text |
| rop-004 | audit-detect-ungated-rules | Rule containing "When editing files in `.claude/skills/`" but no globs frontmatter | Flagged as ungated; suggested glob: `.claude/**` |
| rop-005 | audit-detect-mandatory-reads | Rule with "Read ALL 18 principle files before planning" | Finding lists the instruction and identifies 18 referenced files |


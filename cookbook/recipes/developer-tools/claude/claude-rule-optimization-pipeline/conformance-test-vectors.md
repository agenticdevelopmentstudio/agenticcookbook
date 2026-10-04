
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| rop-001 | audit-inventory-all-rules | `.claude/rules/` with 3 files (50, 100, 200 lines) | Inventory lists all 3 with correct line/byte counts |
| rop-002 | audit-measure-per-turn-cost | 2 ungated rules (100 lines each), 1 globs-scoped rule (50 lines) | Per-turn cost = 200 lines (only ungated rules counted) |
| rop-003 | audit-detect-duplication | 2 rules with identical "Do not skip testing" paragraph | Finding identifies the duplicate with both file paths and matching text |
| rop-004 | audit-detect-ungated-rules | Rule containing "When editing files in `.claude/skills/`" but no globs frontmatter | Flagged as ungated; suggested glob: `.claude/**` |
| rop-005 | audit-detect-mandatory-reads | Rule with "Read ALL 18 principle files before planning" | Finding lists the instruction and identifies 18 referenced files |
| rop-006 | optimize-propose-before-apply | Phase 2 with 3 optimization proposals | All 3 presented to user; no files modified until user confirms |
| rop-007 | optimize-consolidate-overlaps | 2 rules with 40% overlapping content | Proposal specifies which rule retains content, which gets trimmed, expected line reduction |
| rop-008 | optimize-add-globs-scoping | Rule for skill authoring without globs | Proposal adds `globs: .claude/skills/**` frontmatter |
| rop-009 | optimize-extract-to-skills | Rule with 250 lines including a 150-line evaluation checklist | Proposal extracts checklist to a skill, replaces with 1-line pointer |
| rop-010 | optimize-deduplicate-must-nots | Rule body says "You MUST NOT skip Phase 2"; MUST NOT section repeats "Do not skip Phase 2" | Redundant MUST NOT item flagged with body line reference |
| rop-011 | optimize-inline-summaries | Rule mandating read of file that is 65% frontmatter | Proposal replaces mandatory read with inline summary |
| rop-012 | validate-behavioral-preservation | Original has 8 MUST constraints; optimized has 8 equivalent constraints | All 8 mapped and confirmed |
| rop-013 | validate-behavioral-preservation | Original has 8 MUST constraints; optimized has 7 | Validation fails; missing constraint identified |
| rop-014 | validate-lint-each-rule | Optimized rule with vague directive "handle errors appropriately" | Lint FAIL on R04; pipeline blocks until fixed |
| rop-015 | validate-measure-reduction | Before: 381 lines / 17,689 bytes; After: 10 lines / 358 bytes | Reduction: 97.4% lines, 98.0% bytes |
| rop-016 | report-produce-artifact | Completed pipeline run | `.claude/rule-optimization-report.md` exists with all required sections |
| rop-017 | report-idempotent | Pipeline run on rules that already pass all checks | Report says "No optimizations needed"; zero files modified |
| rop-018 | sequential-gating | Attempt to run Phase 3 before Phase 2 completes | Pipeline refuses; error indicates Phase 2 must complete first |
| rop-019 | human-gate-before-writes | Phase 2 with proposals; user declines all | Zero files modified; pipeline proceeds to Phase 4 with "no changes applied" report |


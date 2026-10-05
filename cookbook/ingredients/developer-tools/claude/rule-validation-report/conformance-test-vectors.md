
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| rop-012 | validate-behavioral-preservation | Original has 8 MUST constraints; optimized has 8 equivalent constraints | All 8 mapped and confirmed |
| rop-013 | validate-behavioral-preservation | Original has 8 MUST constraints; optimized has 7 | Validation fails; missing constraint identified |
| rop-014 | validate-lint-each-rule | Optimized rule with vague directive "handle errors appropriately" | Lint FAIL on R04; pipeline blocks until fixed |
| rop-015 | validate-measure-reduction | Before: 381 lines / 17,689 bytes; After: 10 lines / 358 bytes | Reduction: 97.4% lines, 98.0% bytes |
| rop-016 | report-produce-artifact | Completed pipeline run | `.claude/rule-optimization-report.md` exists with all required sections |
| rop-017 | report-idempotent | Pipeline run on rules that already pass all checks | Report says "No optimizations needed"; zero files modified |


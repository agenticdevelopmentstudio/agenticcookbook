
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| rop-018 | sequential-gating | Attempt to run Phase 3 before Phase 2 completes | Pipeline refuses; error indicates Phase 2 must complete first |
| rop-019 | human-gate-before-writes | Phase 2 with proposals; user declines all | Zero files modified; pipeline proceeds to Phase 4 with "no changes applied" report |
| rop-020 | audit-findings-drive-proposals | Audit finds one duplicate paragraph and one ungated rule | The optimizer presents a consolidation proposal and a `globs` proposal, each citing its finding |
| rop-021 | same-measurement-method, baseline-carried-to-report | Run the full pipeline on rules that lose 100 lines | The report's before and after use the same method and its before values equal the audit's output |
| rop-022 | validation-failure-halts | An optimization drops one MUST constraint | Validation fails, no report claims "Optimized", and the outcome is Validation Failed |

Vectors rop-001 to rop-005 (audit), rop-006 to rop-011 (optimizer), and rop-012 to rop-017 (validation and report) are single-ingredient vectors and appear in the ingredients under their original IDs.


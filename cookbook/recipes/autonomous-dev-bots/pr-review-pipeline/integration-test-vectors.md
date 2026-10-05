
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| prp-001 | structural-validation, rejection-format | PR adding a recipe with missing `id` field | Phase 1 rejects, posts review requesting fix |
| prp-002 | overlap-detection, rejection-format | PR adding a recipe with requirements duplicating an existing recipe | Phase 2 flags overlap, suggests consolidation |
| prp-003 | ecosystem-fit, phase-findings-flow-forward | PR modifying a recipe domain without updating references | Phase 3 detects broken cross-references |
| prp-004 | short-circuit, sequential-phases | PR failing Phase 1 | Phase 2 and 3 do not run |
| prp-005 | fix-preference-honored, fixes-come-from-fix-agent | PR with auto-fix enabled, fixable Phase 1 issue | Fix bot pushes corrected commit |
| prp-006 | rerun-on-update, rerun-after-fix | Fix bot pushes a commit to the PR branch | The pipeline restarts from Phase 1 on the new commit |
| prp-007 | appeal-process | Contributor replies to a rejection disputing it | The PR is flagged for human review and no automatic rerun happens |
| prp-008 | branch-protection | All three phase bots approve, no human has approved | Merge is blocked until a human reviewer approves |

The `Requirements` column of prp-003 originally named `cross-reference-integrity`, prp-001 named `recipe-validation, frontmatter-check`, prp-002 named `overlap-detection`, prp-004 named `short-circuit-rejection`, and prp-005 named `auto-fix-preference`; these are the earlier labels for the named requirements now listed above.


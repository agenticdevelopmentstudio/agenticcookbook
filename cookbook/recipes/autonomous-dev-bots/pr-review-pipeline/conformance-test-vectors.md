
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| prp-001 | recipe-validation, frontmatter-check | PR adding a recipe with missing `id` field | Phase 1 rejects, posts review requesting fix |
| prp-002 | overlap-detection | PR adding a recipe with requirements duplicating an existing recipe | Phase 2 flags overlap, suggests consolidation |
| prp-003 | cross-reference-integrity | PR modifying a recipe domain without updating references | Phase 3 detects broken cross-references |
| prp-004 | short-circuit-rejection | PR failing Phase 1 | Phase 2 and 3 do not run |
| prp-005 | auto-fix-preference | PR with auto-fix enabled, fixable Phase 1 issue | Fix bot pushes corrected commit |


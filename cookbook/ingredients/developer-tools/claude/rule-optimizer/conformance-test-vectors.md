
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| rop-006 | optimize-propose-before-apply | Phase 2 with 3 optimization proposals | All 3 presented to user; no files modified until user confirms |
| rop-007 | optimize-consolidate-overlaps | 2 rules with 40% overlapping content | Proposal specifies which rule retains content, which gets trimmed, expected line reduction |
| rop-008 | optimize-add-globs-scoping | Rule for skill authoring without globs | Proposal adds `globs: .claude/skills/**` frontmatter |
| rop-009 | optimize-extract-to-skills | Rule with 250 lines including a 150-line evaluation checklist | Proposal extracts checklist to a skill, replaces with 1-line pointer |
| rop-010 | optimize-deduplicate-must-nots | Rule body says "You MUST NOT skip Phase 2"; MUST NOT section repeats "Do not skip Phase 2" | Redundant MUST NOT item flagged with body line reference |
| rop-011 | optimize-inline-summaries | Rule mandating read of file that is 65% frontmatter | Proposal replaces mandatory read with inline summary |


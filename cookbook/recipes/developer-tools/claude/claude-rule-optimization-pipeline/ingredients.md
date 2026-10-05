
| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Rule audit | `agenticdevelopercookbook://ingredients/developer-tools/claude/rule-audit` | Phase 1: inventory, per-turn cost, duplication, ungated rules, mandatory external reads | Yes | Optional additional rule paths beyond `.claude/rules/` and `rules/` |
| Rule optimizer | `agenticdevelopercookbook://ingredients/developer-tools/claude/rule-optimizer` | Phase 2: proposals for consolidation, `globs` scoping, skill extraction, MUST NOT deduplication, inline summaries; applies only after confirmation | Yes | Extraction threshold (200 lines), frontmatter ratio threshold (50%) |
| Rule validation and report | `agenticdevelopercookbook://ingredients/developer-tools/claude/rule-validation-report` | Phases 3 and 4: behavioral preservation, lint of each rule, reduction measurement, report file | Yes | Report path `.claude/rule-optimization-report.md` |


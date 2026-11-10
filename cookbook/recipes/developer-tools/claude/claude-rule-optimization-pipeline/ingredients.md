
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Rule audit | [adc.ingredient.developer-tools.claude.rule-audit](cookbook:d75d4274-c37b-426a-97f7-69f01e266cc5) | Phase 1: inventory, per-turn cost, duplication, ungated rules, mandatory external reads | Yes | Optional additional rule paths beyond `.claude/rules/` and `rules/` |
| Rule optimizer | [adc.ingredient.developer-tools.claude.rule-optimizer](cookbook:2307a9fe-7721-4c13-bbeb-5320f3ea775d) | Phase 2: proposals for consolidation, `globs` scoping, skill extraction, MUST NOT deduplication, inline summaries; applies only after confirmation | Yes | Extraction threshold (200 lines), frontmatter ratio threshold (50%) |
| Rule validation and report | [adc.ingredient.developer-tools.claude.rule-validation-report](cookbook:5676e038-c4f2-49b5-a8ab-ec3e54e83afb) | Phases 3 and 4: behavioral preservation, lint of each rule, reduction measurement, report file | Yes | Report path `.claude/rule-optimization-report.md` |


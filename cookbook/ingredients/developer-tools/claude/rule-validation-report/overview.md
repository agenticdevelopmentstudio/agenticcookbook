
Rule validation and reporting is the closing half of rule optimization. After the optimizer has changed rule files, it verifies that every original MUST, MUST NOT, and SHOULD constraint survives, runs the lint-rule checklist on each optimized rule, re-measures per-turn cost against the audit baseline, and writes the result to `.claude/rule-optimization-report.md`. Running it on already-optimized rules produces a report that says no changes are needed.

### Pipeline Outcomes

| Outcome | Description | Next Action |
|---------|-------------|-------------|
| Optimized | Rules had measurable waste; optimizations applied, validated, reported | User reviews report, commits changes |
| Already Optimal | All rules pass audit with no actionable findings | Report confirms current state is clean |
| Partially Optimized | Some optimizations applied, others declined or infeasible | Report lists applied and skipped items |
| Validation Failed | Optimizations broke a behavioral constraint or lint check | Pipeline halts; user must fix or revert |

### Metrics Collected

| Metric | ID | Unit | Collected In |
|--------|----|------|-------------|
| Per-turn cost (lines) | `per-turn-lines` | integer | Audit, Validate |
| Per-turn cost (bytes) | `per-turn-bytes` | integer | Audit, Validate |
| Rule file count | `rule-count` | integer | Audit, Validate |
| Mandatory external reads | `mandatory-reads` | integer | Audit, Validate |
| Reduction percentage | `reduction-pct` | percentage | Validate |

### Privacy

- **Data collected**: None
- **Storage**: Report file stored locally at `.claude/rule-optimization-report.md`
- **Transmission**: No data leaves the device
- **Retention**: Report persists until manually deleted or overwritten by next pipeline run


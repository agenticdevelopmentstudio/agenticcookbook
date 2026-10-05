
Claude Code rule files in `.claude/rules/` are injected into the system prompt on every turn — not just at session start. A 200-line rule costs 200 lines × N turns per session. The agenticdevelopercookbook's own rules went from 381 lines / 17,689 bytes per turn to 10 lines / 358 bytes — a 97% reduction — by applying a systematic optimization pipeline.

This recipe codifies that pipeline into four repeatable phases, composed from three ingredients:

1. **Audit** — inventory rules, measure per-turn cost, detect waste (rule audit)
2. **Optimize** — propose and apply context-reduction strategies (rule optimizer)
3. **Validate** — verify behavioral preservation and run lint checks (rule validation and report)
4. **Report** — produce before/after metrics (rule validation and report)

The pipeline is sequential: each phase gates the next. Phase 2 (Optimize) requires explicit user confirmation before modifying any files — rule files are behavioral guardrails and MUST NOT be changed autonomously.

### Pipeline Outcomes

| Outcome | Description | Next Action |
|---------|-------------|-------------|
| Optimized | Rules had measurable waste; optimizations applied, validated, reported | User reviews report, commits changes |
| Already Optimal | All rules pass audit with no actionable findings | Report confirms current state is clean |
| Partially Optimized | Some optimizations applied, others declined or infeasible | Report lists applied and skipped items |
| Validation Failed | Optimizations broke a behavioral constraint or lint check | Pipeline halts; user must fix or revert |

### Metrics

| Metric | ID | Unit | Collected In |
|--------|----|------|-------------|
| Per-turn cost (lines) | `per-turn-lines` | integer | Audit, Validate |
| Per-turn cost (bytes) | `per-turn-bytes` | integer | Audit, Validate |
| Rule file count | `rule-count` | integer | Audit, Validate |
| Mandatory external reads | `mandatory-reads` | integer | Audit, Validate |
| Duplication ratio | `duplication-ratio` | percentage | Audit |
| Ungated rule count | `ungated-count` | integer | Audit |
| Redundant MUST NOT count | `redundant-must-nots` | integer | Audit |
| Frontmatter-heavy refs | `high-metadata-refs` | integer | Audit |
| Reduction percentage | `reduction-pct` | percentage | Validate |

### Sections that do not apply

The original recipe recorded these sections as not applicable, and the statements still hold for the composition: Deep Linking (CLI pipeline, not a navigable resource), Localization (no user-facing strings), Accessibility Options (CLI pipeline), Feature Flags (the pipeline is invoked explicitly, not gated), Analytics (local CLI pipeline, no telemetry), Accessibility (CLI pipeline, no visual UI), and Logging (output is produced through the report file, not log messages).

### Privacy

The Privacy statement lives in the rule validation and report ingredient, which writes the only artifact: no data is collected, the report is stored locally at `.claude/rule-optimization-report.md`, no data leaves the device, and the report persists until manually deleted or overwritten by the next run.

### Appearance of the report

The pipeline's visible output is the report file; its heading structure, metrics tables, changes list, and lint results are specified in the rule validation and report ingredient's Appearance section.

### States

| State | How to detect | Behavior |
|-------|---------------|----------|
| Auditing | Phase 1 output being produced | Read-only inventory and measurement; no user interaction required |
| Awaiting Confirmation | Phase 2 proposals presented | Pipeline paused; user must confirm, decline, or selectively approve optimizations |
| Optimizing | User confirmed; files being modified | Rule files updated per approved proposals |
| Validating | Phase 3 checks running | Behavioral preservation enumeration and lint-rule checks; read-only |
| Reporting | Phase 4 report being written | Report file created at `.claude/rule-optimization-report.md` |
| Complete | Report file exists; pipeline finished | No further action; user reviews report |
| Failed | Validation found missing constraint or lint FAIL | Pipeline halted; user must fix or revert before re-running |


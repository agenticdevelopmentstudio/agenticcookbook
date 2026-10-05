---
id: 5676E038-C4F2-49B5-A8AB-EC3E54E83AFB
title: "Rule Validation and Report"
domain: agenticdevelopercookbook://ingredients/developer-tools/claude/rule-validation-report
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Verifies behavioral preservation and lint results for optimized rules, measures the reduction, and writes the before/after report file"
platforms:
  - macos
  - linux
  - windows
tags:
  - claude-code
  - rules
  - validation
  - report
depends-on:
  - agenticdevelopercookbook://ingredients/developer-tools/claude/rule-audit
  - agenticdevelopercookbook://ingredients/developer-tools/claude/rule-optimizer
related:
  - agenticdevelopercookbook://recipes/developer-tools/claude/claude-rule-optimization-pipeline
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Rule Validation and Report

## Overview

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

## Behavioral Requirements

### Validate

- **validate-behavioral-preservation**: After optimizations are applied, the pipeline MUST verify that every behavioral constraint from the original rules is present in the optimized output. The pipeline MUST enumerate each original MUST, MUST NOT, and SHOULD constraint and confirm its presence (exact or equivalent) in the optimized files.
- **validate-lint-each-rule**: The pipeline MUST run the lint-rule checklist (all C-series, B-series, R-series, and O-series checks) against each optimized rule file. Any FAIL result MUST block the pipeline from proceeding to Phase 4 until resolved.
- **validate-measure-reduction**: The pipeline MUST re-measure per-turn cost using the same method as audit-measure-per-turn-cost and calculate the percentage reduction from the audit baseline.

### Report

- **report-produce-artifact**: The pipeline MUST produce a report file at `.claude/rule-optimization-report.md` containing: timestamp, before metrics (from Phase 1), after metrics (from Phase 3), percentage reduction, list of changes applied, lint results per file, and any constraints that could not be optimized further.
- **report-idempotent**: Running the pipeline again on already-optimized rules MUST produce a report showing no changes needed rather than making unnecessary modifications.

## Appearance

The pipeline's visible output is the report file at `.claude/rule-optimization-report.md`:

- **Heading structure**: H1 title, H2 per section (Timestamp, Before Metrics, After Metrics, Reduction, Changes Applied, Lint Results, Notes)
- **Metrics tables**: Markdown tables with columns: Metric | Before | After | Change
- **Changes list**: Bulleted list, one item per optimization applied, with file path and description
- **Lint results**: One H3 per rule file, followed by the lint-rule checklist results (PASS/WARN/FAIL per check)

## States

| State | How to detect | Behavior |
|-------|---------------|----------|
| Validating | Validation checks running | Behavioral preservation enumeration and lint-rule checks; read-only |
| Reporting | Report being written | Report file created at `.claude/rule-optimization-report.md` |
| Complete | Report file exists; pipeline finished | No further action; user reviews report |
| Failed | Validation found missing constraint or lint FAIL | Pipeline halted; user must fix or revert before re-running |

## Accessibility

Not applicable — the report is a markdown file with no interactive UI; its heading and table structure are standard accessible markdown.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| rop-012 | validate-behavioral-preservation | Original has 8 MUST constraints; optimized has 8 equivalent constraints | All 8 mapped and confirmed |
| rop-013 | validate-behavioral-preservation | Original has 8 MUST constraints; optimized has 7 | Validation fails; missing constraint identified |
| rop-014 | validate-lint-each-rule | Optimized rule with vague directive "handle errors appropriately" | Lint FAIL on R04; pipeline blocks until fixed |
| rop-015 | validate-measure-reduction | Before: 381 lines / 17,689 bytes; After: 10 lines / 358 bytes | Reduction: 97.4% lines, 98.0% bytes |
| rop-016 | report-produce-artifact | Completed pipeline run | `.claude/rule-optimization-report.md` exists with all required sections |
| rop-017 | report-idempotent | Pipeline run on rules that already pass all checks | Report says "No optimizations needed"; zero files modified |

## Edge Cases

- **Empty rules directory**: With no rules found, the report MUST say "No rules found."
- **Sensitive content in rules**: The report MUST NOT include literal file content that might expose credentials or internal paths beyond what is necessary to describe the optimization.
- **User declined everything**: The report documents the proposals and the decision to decline, with "no changes applied."

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| Report path | string | `.claude/rule-optimization-report.md` | Where the report is written |

## Logging

Not applicable — output is delivered through the report file, not log messages.

## Platform Notes

- **macOS/Linux/Windows**: The report path is project-relative; line and byte counts use the same method as the audit (`wc -l`, `wc -c` or equivalent).
- **SwiftUI / Compose / React/Web**: Not applicable — CLI step with no UI framework.

## Design Decisions

**Decision**: Report file as primary output, not PR comment.
**Rationale**: The report is useful as a standalone artifact that can be committed alongside optimized rules. Not all optimization runs happen in a PR context (e.g., local development, initial setup). A future extension can post the report as a PR comment when the pipeline runs in CI.
**Approved**: pending

**Decision**: Reuse lint-rule O-series checks rather than defining new validation logic.
**Rationale**: The O-series checks already encode optimization criteria from the rule-optimization research. Reusing them avoids duplication and ensures the pipeline and linter stay in sync.
**Approved**: pending

**Decision**: Enumeration-based behavioral validation.
**Rationale**: Each original MUST/MUST NOT/SHOULD constraint gets mapped to its optimized equivalent. If a constraint cannot be mapped, validation fails with a specific gap identified. This is more reliable than abstract semantic comparison.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [data-minimization](agenticdevelopercookbook://compliance/privacy-and-data#data-minimization) | partial | Privacy |
| [secure-log-output](agenticdevelopercookbook://compliance/security#secure-log-output) | partial | Security |
| [idempotent-operations](agenticdevelopercookbook://compliance/reliability#idempotent-operations) | partial | Reliability |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Claude Rule Optimization Pipeline recipe |

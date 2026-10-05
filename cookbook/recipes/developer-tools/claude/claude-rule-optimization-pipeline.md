---
id: aa81d10d-38d1-40d4-8be4-212b043e6410
title: "Claude Rule Optimization Pipeline"
domain: agenticdevelopercookbook://recipes/developer-tools/claude/claude-rule-optimization-pipeline
type: recipe
version: 2.0.0
status: accepted
language: en
created: 2026-03-30
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Four-phase pipeline for auditing, optimizing, validating, and reporting on Claude Code rule file context efficiency."
platforms:
  - macos
  - linux
  - windows
tags:
  - claude-code
  - rules
  - optimization
  - context-efficiency
  - pipeline
ingredients:
  - agenticdevelopercookbook://ingredients/developer-tools/claude/rule-audit
  - agenticdevelopercookbook://ingredients/developer-tools/claude/rule-optimizer
  - agenticdevelopercookbook://ingredients/developer-tools/claude/rule-validation-report
depends-on: []
related:
  - agenticdevelopercookbook://ingredients/developer-tools/claude/yolo-mode
  - agenticdevelopercookbook://recipes/autonomous-dev-bots/pr-review-pipeline
references:
  - https://code.claude.com/docs/en/best-practices
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Claude Rule Optimization Pipeline

## Overview

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

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Rule audit | `agenticdevelopercookbook://ingredients/developer-tools/claude/rule-audit` | Phase 1: inventory, per-turn cost, duplication, ungated rules, mandatory external reads | Yes | Optional additional rule paths beyond `.claude/rules/` and `rules/` |
| Rule optimizer | `agenticdevelopercookbook://ingredients/developer-tools/claude/rule-optimizer` | Phase 2: proposals for consolidation, `globs` scoping, skill extraction, MUST NOT deduplication, inline summaries; applies only after confirmation | Yes | Extraction threshold (200 lines), frontmatter ratio threshold (50%) |
| Rule validation and report | `agenticdevelopercookbook://ingredients/developer-tools/claude/rule-validation-report` | Phases 3 and 4: behavioral preservation, lint of each rule, reduction measurement, report file | Yes | Report path `.claude/rule-optimization-report.md` |

## Integration Requirements

- **sequential-gating**: Phases MUST execute in order: 1 → 2 → 3 → 4. A phase MUST NOT start until the previous phase completes successfully.
- **human-gate-before-writes**: The pipeline MUST NOT modify any rule file without explicit user confirmation. Phases 1 and 4 are read-only. Phase 2 requires confirmation. Phase 3 re-validates after writes.
- **audit-findings-drive-proposals**: The rule optimizer MUST build its proposals only from the rule audit's findings (duplication, ungated rules, mandatory reads), and every proposal MUST cite the finding that motivated it.
- **same-measurement-method**: The validation phase MUST measure per-turn cost with the same method as the audit so the before and after numbers in the report are comparable.
- **baseline-carried-to-report**: The audit's before metrics MUST be carried unchanged to the report, even when the user declines every optimization.
- **validation-failure-halts**: A behavioral-preservation failure or a lint FAIL in the validation phase MUST halt the pipeline before the report phase writes an "optimized" outcome, and the pipeline outcome MUST be recorded as Validation Failed.

## Layout

This is a CLI pipeline with no visual UI, so the layout is the order of the phases and which of them may write.

```
 ┌───────────────┐   findings   ┌────────────────┐  confirmed edits  ┌───────────────────────────┐
 │ 1 Rule audit  │ ───────────▶ │ 2 Rule         │ ────────────────▶ │ 3 Validate (rule          │
 │ read-only     │              │ optimizer      │   (human gate)    │   validation and report)  │
 └───────────────┘              │ proposes, then │                   │ re-measure + lint         │
                                │ writes if OK'd │                   └─────────────┬─────────────┘
                                └────────────────┘                                 │ pass
                                                                      ┌────────────▼────────────┐
                                                                      │ 4 Report (read-only)    │
                                                                      │ .claude/rule-           │
                                                                      │   optimization-report.md│
                                                                      └─────────────────────────┘
```

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| Rule inventory and baseline metrics | Rule audit | Rule optimizer, report | one-way | Held in conversation context for the run |
| Audit findings | Rule audit | Rule optimizer | one-way | Duplication, ungated, and mandatory-read findings listed with file locations |
| Approved proposals | User via the rule optimizer | Rule optimizer write step | one-way | Explicit confirmation of each proposal, or a decline of all |
| Original constraint list | Rule files before edits | Validation | one-way | The enumerated MUST, MUST NOT, and SHOULD constraints captured before writes |
| After metrics and reduction percentage | Validation | Report | one-way | Re-measurement by the same method as the audit |
| Report file | Report phase | The user | one-way | Written to `.claude/rule-optimization-report.md` |

Pipeline state lives in conversation context, not on disk (see Design Decisions): an interrupted run restarts from Phase 1.

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| rop-018 | sequential-gating | Attempt to run Phase 3 before Phase 2 completes | Pipeline refuses; error indicates Phase 2 must complete first |
| rop-019 | human-gate-before-writes | Phase 2 with proposals; user declines all | Zero files modified; pipeline proceeds to Phase 4 with "no changes applied" report |
| rop-020 | audit-findings-drive-proposals | Audit finds one duplicate paragraph and one ungated rule | The optimizer presents a consolidation proposal and a `globs` proposal, each citing its finding |
| rop-021 | same-measurement-method, baseline-carried-to-report | Run the full pipeline on rules that lose 100 lines | The report's before and after use the same method and its before values equal the audit's output |
| rop-022 | validation-failure-halts | An optimization drops one MUST constraint | Validation fails, no report claims "Optimized", and the outcome is Validation Failed |

Vectors rop-001 to rop-005 (audit), rop-006 to rop-011 (optimizer), and rop-012 to rop-017 (validation and report) are single-ingredient vectors and appear in the ingredients under their original IDs.

## Edge Cases

- **Empty rules directory**: `.claude/rules/` exists but contains no `.md` files. The pipeline MUST complete Phase 1 with zero metrics and skip Phases 2–3, producing a Phase 4 report that says "No rules found."
- **Single rule, already optimal**: One rule file under 50 lines, no duplication, has globs, clean MUST NOTs. The pipeline MUST complete all 4 phases, with Phase 2 reporting "No optimizations proposed."
- **Non-markdown files**: `.claude/rules/` may contain `.json`, `.yaml`, `.sh`, or other files. The pipeline MUST ignore non-`.md` files during inventory.
- **Broken file references**: A rule mandates reading a file that no longer exists. The audit MUST flag this as a separate finding (broken reference) distinct from optimization concerns.
- **Overly broad globs**: A rule has `globs: **` (matches everything, effectively ungated). The pipeline MUST treat this the same as no globs and suggest narrowing.
- **Circular references**: Rule A says "see rule B" and rule B says "see rule A." The deduplication check MUST handle this without infinite loops.
- **Custom rule paths**: Some projects put rules in non-standard paths referenced from `CLAUDE.md`. The pipeline SHOULD accept an optional path argument to scan additional directories.
- **Very large single rule (500+ lines)**: The pipeline MUST still complete successfully and SHOULD propose splitting into a minimal always-on section plus one or more skills, identifying natural section boundaries.
- **User declines all optimizations**: Phase 2 proposes changes, user declines everything. Pipeline MUST proceed to Phase 4 with a report documenting the proposals and the decision to decline.
- **Sensitive content in rules**: The report MUST NOT include literal file content that might expose credentials or internal paths beyond what is necessary to describe the optimization.

## Platform Notes

- **macOS/Linux**: Rule files in `.claude/rules/` follow standard POSIX paths. File size measured with `wc -c`, line count with `wc -l`.
- **Windows**: Rule files use the same `.claude/rules/` path relative to the project root. File operations work via Git Bash, WSL, or any POSIX-compatible shell.
- **SwiftUI / Compose / React/Web**: Not applicable — the pipeline is a CLI workflow with no UI framework.

## Design Decisions

- **Guided pipeline with human gate, not fully autonomous**: Rule files are behavioral guardrails — they control what Claude does and does not do. Autonomously modifying guardrails risks weakening safety constraints. The pr-review-pipeline is autonomous because it only reads and comments; this pipeline writes, so user confirmation is required before any modification. **Approved**: pending
- **Report file as primary output, not PR comment**: The report is useful as a standalone artifact that can be committed alongside optimized rules. Not all optimization runs happen in a PR context (e.g., local development, initial setup). A future extension can post the report as a PR comment when the pipeline runs in CI. **Approved**: pending
- **Reuse lint-rule O-series checks rather than defining new validation logic**: The O-series checks already encode optimization criteria from the rule-optimization research. Reusing them avoids duplication and ensures the pipeline and linter stay in sync. **Approved**: pending
- **Measure per-turn cost in both lines and bytes**: Lines are human-readable and easy to reason about. Bytes are the actual context window cost. Both metrics appear throughout the optimization research. Reporting both gives complementary perspectives. **Approved**: pending
- **Enumeration-based behavioral validation**: Each original MUST/MUST NOT/SHOULD constraint gets mapped to its optimized equivalent. If a constraint cannot be mapped, validation fails with a specific gap identified. This is more reliable than abstract semantic comparison. **Approved**: pending
- **Pipeline state in conversation context, not on disk**: Unlike `/cookbook-next` which spans many turns and benefits from disk-persisted state, this pipeline runs in a single focused session (typically 10–20 turns). Conversation context is sufficient. If interrupted, the pipeline restarts from Phase 1 — safe because Phase 1 is read-only and Phase 2 requires re-confirmation. **Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [safe-defaults](agenticdevelopercookbook://compliance/user-safety#safe-defaults) | partial | User Safety |
| [data-minimization](agenticdevelopercookbook://compliance/privacy-and-data#data-minimization) | partial | Privacy |
| [secure-log-output](agenticdevelopercookbook://compliance/security#secure-log-output) | partial | Security |
| [idempotent-operations](agenticdevelopercookbook://compliance/reliability#idempotent-operations) | partial | Reliability |
| [fault-tolerance](agenticdevelopercookbook://compliance/reliability#fault-tolerance) | partial | Reliability |

> Status is `partial`: this recipe specifies the integration-level requirements that satisfy these checks, but compliance is verified per concrete pipeline run, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-10-04 | Mike Fullerton | Restructure into recipe shape; extract component behavior into ingredients |
| 1.0.0 | 2026-03-30 | Mike Fullerton | Initial creation |

---
id: 2307A9FE-7721-4C13-BBEB-5320F3EA775D
title: "Rule Optimizer"
domain: agenticdevelopercookbook://ingredients/developer-tools/claude/rule-optimizer
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Proposes and, on explicit user confirmation, applies context-reduction strategies to Claude Code rule files"
platforms:
  - macos
  - linux
  - windows
tags:
  - claude-code
  - rules
  - optimization
  - context-efficiency
depends-on:
  - agenticdevelopercookbook://ingredients/developer-tools/claude/rule-audit
related:
  - agenticdevelopercookbook://recipes/developer-tools/claude/claude-rule-optimization-pipeline
  - agenticdevelopercookbook://ingredients/developer-tools/claude/rule-validation-report
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Rule Optimizer

## Overview

The rule optimizer turns the rule audit's findings into concrete context-reduction proposals: consolidate overlapping content, scope rules with `globs`, extract workflow content to on-demand skills, drop redundant MUST NOT items, and replace metadata-heavy mandatory reads with inline summaries. Rule files are behavioral guardrails, so the optimizer never writes a file until the user has explicitly confirmed the specific proposals.

## Behavioral Requirements

- **optimize-propose-before-apply**: The pipeline MUST present all proposed optimizations to the user and wait for explicit confirmation before modifying any files. Each proposal MUST state what will change, the expected per-turn cost reduction, and any behavioral impact.
- **optimize-consolidate-overlaps**: When audit-detect-duplication found overlapping content, the pipeline MUST propose consolidating into a single rule file or extracting shared content to a referenced file. The proposal MUST specify which file retains the content and which files get trimmed.
- **optimize-add-globs-scoping**: For each rule flagged by audit-detect-ungated-rules, the pipeline MUST propose adding `globs` frontmatter with the narrowest pattern that covers the rule's intended scope.
- **optimize-extract-to-skills**: When a rule file exceeds 200 lines or contains workflow content (multi-step procedures, checklists, evaluation criteria), the pipeline SHOULD propose extracting that content to an on-demand skill, replacing it with a one-line skill pointer in the rule.
- **optimize-deduplicate-must-nots**: The pipeline MUST scan each rule's MUST NOT section and flag items that restate constraints already expressed imperatively in the rule body. The proposal MUST list each redundant item with the body line it duplicates.
- **optimize-inline-summaries**: When audit-detect-mandatory-reads found external files with a frontmatter-to-content ratio exceeding 50%, the pipeline SHOULD propose replacing the mandatory read with an inline summary and an optional file path for reference.

## Appearance

Not applicable — the optimizer is a CLI step with no visual UI; proposals are presented as conversation text.

## States

| State | How to detect | Behavior |
|-------|---------------|----------|
| Awaiting Confirmation | Proposals presented | Pipeline paused; user must confirm, decline, or selectively approve optimizations |
| Optimizing | User confirmed; files being modified | Rule files updated per approved proposals |

## Accessibility

Not applicable — CLI step, no visual UI.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| rop-006 | optimize-propose-before-apply | Phase 2 with 3 optimization proposals | All 3 presented to user; no files modified until user confirms |
| rop-007 | optimize-consolidate-overlaps | 2 rules with 40% overlapping content | Proposal specifies which rule retains content, which gets trimmed, expected line reduction |
| rop-008 | optimize-add-globs-scoping | Rule for skill authoring without globs | Proposal adds `globs: .claude/skills/**` frontmatter |
| rop-009 | optimize-extract-to-skills | Rule with 250 lines including a 150-line evaluation checklist | Proposal extracts checklist to a skill, replaces with 1-line pointer |
| rop-010 | optimize-deduplicate-must-nots | Rule body says "You MUST NOT skip Phase 2"; MUST NOT section repeats "Do not skip Phase 2" | Redundant MUST NOT item flagged with body line reference |
| rop-011 | optimize-inline-summaries | Rule mandating read of file that is 65% frontmatter | Proposal replaces mandatory read with inline summary |

## Edge Cases

- **Single rule, already optimal**: One rule file under 50 lines, no duplication, has globs, clean MUST NOTs. The optimizer MUST report "No optimizations proposed."
- **Overly broad globs**: A rule with `globs: **` is treated as ungated and the optimizer suggests narrowing.
- **Very large single rule (500+ lines)**: The optimizer SHOULD propose splitting into a minimal always-on section plus one or more skills, identifying natural section boundaries.
- **User declines all optimizations**: The optimizer proposes changes, the user declines everything. The pipeline MUST proceed to the report with a record of the proposals and the decision to decline.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| Extraction threshold | integer (lines) | 200 | Rule size above which extraction to a skill is proposed |
| Frontmatter ratio threshold | percentage | 50 | Frontmatter-to-content ratio above which a mandatory read is replaced by an inline summary |

## Logging

Not applicable — the optimizer's output is delivered through the pipeline report file, not log messages.

## Platform Notes

- **macOS/Linux/Windows**: Edits rule files with ordinary file writes at the project-relative `.claude/rules/` path.
- **SwiftUI / Compose / React/Web**: Not applicable — CLI step with no UI framework.

## Design Decisions

**Decision**: Guided pipeline with human gate, not fully autonomous.
**Rationale**: Rule files are behavioral guardrails — they control what Claude does and does not do. Autonomously modifying guardrails risks weakening safety constraints. The pr-review-pipeline is autonomous because it only reads and comments; this pipeline writes, so user confirmation is required before any modification.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [safe-defaults](agenticdevelopercookbook://compliance/user-safety#safe-defaults) | partial | User Safety |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Claude Rule Optimization Pipeline recipe |

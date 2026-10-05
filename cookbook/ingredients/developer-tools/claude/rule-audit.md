---
id: D75D4274-C37B-426A-97F7-69F01E266CC5
title: "Rule Audit"
domain: agenticdevelopercookbook://ingredients/developer-tools/claude/rule-audit
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Read-only audit of Claude Code rule files that inventories them, measures per-turn context cost, and detects duplication, ungated rules, and mandatory external reads"
platforms:
  - macos
  - linux
  - windows
tags:
  - claude-code
  - rules
  - audit
  - context-efficiency
depends-on: []
related:
  - agenticdevelopercookbook://recipes/developer-tools/claude/claude-rule-optimization-pipeline
  - agenticdevelopercookbook://ingredients/developer-tools/claude/rule-optimizer
references:
  - https://code.claude.com/docs/en/best-practices
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Rule Audit

## Overview

Claude Code rule files in `.claude/rules/` are injected into the system prompt on every turn, so a 200-line rule costs 200 lines times the number of turns in a session. The rule audit is the read-only first phase of rule optimization: it inventories every rule file, measures the aggregate per-turn cost, and finds the waste (duplicated constraints, rules that should be scoped by `globs`, and instructions that force external file reads). It changes nothing; its findings feed the rule optimizer.

### Metrics Collected

| Metric | ID | Unit |
|--------|----|------|
| Per-turn cost (lines) | `per-turn-lines` | integer |
| Per-turn cost (bytes) | `per-turn-bytes` | integer |
| Rule file count | `rule-count` | integer |
| Mandatory external reads | `mandatory-reads` | integer |
| Duplication ratio | `duplication-ratio` | percentage |
| Ungated rule count | `ungated-count` | integer |
| Redundant MUST NOT count | `redundant-must-nots` | integer |
| Frontmatter-heavy refs | `high-metadata-refs` | integer |

## Behavioral Requirements

- **audit-inventory-all-rules**: The pipeline MUST inventory every `.md` file in `.claude/rules/` (and `rules/` if present), recording the file path, line count, and byte size of each.
- **audit-measure-per-turn-cost**: The pipeline MUST calculate the aggregate per-turn cost: the sum of lines and bytes across all rule files that load without `globs` restrictions. Rules with `globs` frontmatter that would not match a generic file context MUST be excluded from the per-turn total.
- **audit-detect-duplication**: The pipeline MUST compare all rule files pairwise and identify paragraphs, list items, or sections that express the same constraint. A finding MUST include the overlapping text and both file locations.
- **audit-detect-ungated-rules**: The pipeline MUST flag any rule file that applies only to a specific file pattern (identifiable by content referencing specific directories or file types) but lacks `globs` frontmatter.
- **audit-detect-mandatory-reads**: The pipeline MUST identify every instruction in rule files that mandates reading external files (patterns: "read", "load", "review", "check" followed by a file path or glob). Each finding MUST record the rule file, the instruction, and the referenced file paths.

## Appearance

Not applicable — the audit is a CLI analysis with no visual UI; its findings appear in the pipeline report.

## States

| State | How to detect | Behavior |
|-------|---------------|----------|
| Auditing | Audit output being produced | Read-only inventory and measurement; no user interaction required |

## Accessibility

Not applicable — CLI analysis, no visual UI.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| rop-001 | audit-inventory-all-rules | `.claude/rules/` with 3 files (50, 100, 200 lines) | Inventory lists all 3 with correct line/byte counts |
| rop-002 | audit-measure-per-turn-cost | 2 ungated rules (100 lines each), 1 globs-scoped rule (50 lines) | Per-turn cost = 200 lines (only ungated rules counted) |
| rop-003 | audit-detect-duplication | 2 rules with identical "Do not skip testing" paragraph | Finding identifies the duplicate with both file paths and matching text |
| rop-004 | audit-detect-ungated-rules | Rule containing "When editing files in `.claude/skills/`" but no globs frontmatter | Flagged as ungated; suggested glob: `.claude/**` |
| rop-005 | audit-detect-mandatory-reads | Rule with "Read ALL 18 principle files before planning" | Finding lists the instruction and identifies 18 referenced files |

## Edge Cases

- **Empty rules directory**: `.claude/rules/` exists but contains no `.md` files. The audit MUST complete with zero metrics so the pipeline can report "No rules found."
- **Non-markdown files**: `.claude/rules/` may contain `.json`, `.yaml`, `.sh`, or other files. The audit MUST ignore non-`.md` files during inventory.
- **Broken file references**: A rule mandates reading a file that no longer exists. The audit MUST flag this as a separate finding (broken reference) distinct from optimization concerns.
- **Overly broad globs**: A rule has `globs: **` (matches everything, effectively ungated). The audit MUST treat this the same as no globs.
- **Circular references**: Rule A says "see rule B" and rule B says "see rule A." Duplication detection MUST handle this without infinite loops.
- **Custom rule paths**: Some projects put rules in non-standard paths referenced from `CLAUDE.md`. The audit SHOULD accept an optional path argument to scan additional directories.
- **Very large single rule (500+ lines)**: The audit MUST still complete successfully.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| Additional rule paths | string[] | none | Extra directories to scan beyond `.claude/rules/` and `rules/` |

## Logging

Not applicable — the audit's output is delivered through the pipeline report file, not log messages.

## Platform Notes

- **macOS/Linux**: Rule files in `.claude/rules/` follow standard POSIX paths. File size measured with `wc -c`, line count with `wc -l`.
- **Windows**: Rule files use the same `.claude/rules/` path relative to the project root. File operations work via Git Bash, WSL, or any POSIX-compatible shell.
- **SwiftUI / Compose / React/Web**: Not applicable — CLI analysis with no UI framework.

## Design Decisions

**Decision**: Measure per-turn cost in both lines and bytes.
**Rationale**: Lines are human-readable and easy to reason about. Bytes are the actual context window cost. Both metrics appear throughout the optimization research. Reporting both gives complementary perspectives.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [fault-tolerance](agenticdevelopercookbook://compliance/reliability#fault-tolerance) | partial | Reliability |
| [resource-efficiency](agenticdevelopercookbook://compliance/performance#resource-efficiency) | partial | Performance |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Claude Rule Optimization Pipeline recipe |

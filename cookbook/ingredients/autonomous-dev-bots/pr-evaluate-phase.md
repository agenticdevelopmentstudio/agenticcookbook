---
id: F48198BB-F5AD-49DD-9342-945AF89A3AB4
title: "PR Evaluate Phase"
domain: agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-evaluate-phase
type: ingredient
version: 1.0.0
status: wip
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Phase 3 of the PR review pipeline: value and risk scoring, external research, and a structured recommendation to the human reviewer"
platforms:
  - macos
tags:
  - automation
  - review
  - evaluation
  - github
depends-on: []
related:
  - agenticdevelopercookbook://recipes/autonomous-dev-bots/pr-review-pipeline
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# PR Evaluate Phase

## Overview

The PR evaluate phase is Phase 3 of the cookbook PR review pipeline, run by the Cookbook Eval Bot (`@cookbook-eval-bot[bot]`). It scores a contribution's value and risk, researches the idea beyond the repository, and posts a structured recommendation. It recommends but never merges: the human reviewer decides.

## Behavioral Requirements

- **value-scoring**: Phase 3 MUST score the contribution on: novelty (fills a gap), demand signal (multiple projects would use this), quality (how clean was the Phase 1/2 pass), completeness (platform coverage, test vector thoroughness), ecosystem integration (quality of depends-on/related links).
- **risk-scoring**: Phase 3 MUST assess: breaking changes to existing content, conflicts with engineering principles, scope appropriateness for the cookbook, contributor track record (first-time vs established).
- **external-research**: Phase 3 MUST research beyond the repo: search GitHub for similar patterns, check platform SDK documentation to see if the concept is built-in, assess whether the pattern is well-established or novel.
- **recommendation**: Phase 3 MUST produce a structured recommendation: value (HIGH/MEDIUM/LOW), confidence (HIGH/MEDIUM/LOW), recommendation (ACCEPT/ACCEPT WITH REFACTORING/PARTIAL ACCEPT/REJECT), with per-section rationale.
- **human-escalation**: Phase 3 MUST post its recommendation as a PR review. The human reviewer makes the final decision — Phase 3 recommends but never merges.

## Appearance

Not applicable — this phase is an automated evaluation with no visual UI; its output is a GitHub PR review rendered by GitHub.

## States

| State | Behavior |
|-------|----------|
| Scoring | Value and risk are being scored from the Phase 1 and Phase 2 findings |
| Researching | External research is running |
| Recommended | The structured recommendation is posted as a PR review |

## Accessibility

Not applicable — the phase interacts through GitHub's PR interface, which provides its own accessible rendering of bot comments.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pr-eval-001 | value-scoring | A contribution that fills a documented gap with full platform coverage | Scores are produced for all five value dimensions |
| pr-eval-002 | risk-scoring | A contribution that renames an existing requirement used elsewhere | Breaking-change risk is reported |
| pr-eval-003 | external-research | A contribution describing a pattern built into a platform SDK | The research finding notes the built-in alternative |
| pr-eval-004 | recommendation | A clean contribution | Output has value, confidence, and one of the four recommendation values with per-section rationale |
| pr-eval-005 | human-escalation | Any completed evaluation | The recommendation is posted as a PR review and the PR is not merged by the bot |

## Edge Cases

- **First-time contributor**: Track record contributes to risk, not to automatic rejection.
- **Research unavailable**: If external search fails, the recommendation MUST state that research was not completed and lower its confidence accordingly.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| Model | string | Claude Opus | Evaluation requires strong reasoning |

## Logging

This ingredient defines no events of its own; the pipeline-level `Pipeline` events (phase completed) cover it.

## Platform Notes

- **macOS (OpenClaw)**: Runs on the OpenClaw host with network access for GitHub search and SDK documentation lookups.
- **SwiftUI / Compose / React/Web**: Not applicable — this is an automation phase with no UI framework.

## Design Decisions

**Decision**: The phase recommends; a human decides.
**Rationale**: Inclusion in the cookbook is a judgment call about direction; the bot supplies scored evidence while the merge decision stays with a person.
**Approved**: yes

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [post-generation-verification](agenticdevelopercookbook://compliance/best-practices#post-generation-verification) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the PR Review Pipeline recipe |

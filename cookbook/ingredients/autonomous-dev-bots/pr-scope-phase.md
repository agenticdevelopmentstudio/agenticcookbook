---
id: 63C5A406-6356-417F-B549-B97E40385BA5
title: "PR Scope Phase"
domain: agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-scope-phase
type: ingredient
version: 1.0.0
status: wip
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Phase 2 of the PR review pipeline: placement, granularity, overlap detection against all cookbook content, ecosystem fit, and per-requirement refactoring proposals"
platforms:
  - macos
tags:
  - automation
  - review
  - scoping
  - github
depends-on: []
related:
  - agenticdevelopercookbook://recipes/autonomous-dev-bots/pr-review-pipeline
  - agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-fix-agent
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# PR Scope Phase

## Overview

The PR scope phase is Phase 2 of the cookbook PR review pipeline, run by the Cookbook Scope Bot (`@cookbook-scope-bot[bot]`). It decides whether a contribution is in the right place, is the right size, and does not duplicate existing cookbook content, and when it is not, it produces a concrete refactoring proposal. It is read-only: it posts a PR review and never edits content (the fix agent applies approved proposals).

## Behavioral Requirements

- **placement-analysis**: Phase 2 MUST verify the recipe is in the correct directory for its type and that the domain identifier matches the file path.
- **granularity-check**: Phase 2 MUST assess whether the recipe covers exactly one coherent concept. Flag recipes with more than 15 MUST requirements or more than 8 states as potentially too broad. Flag recipes with fewer than 3 requirements as potentially too narrow.
- **overlap-detection**: Phase 2 MUST compare the new/changed content against ALL existing cookbook content (principles, guidelines, and recipes) for conceptual overlap. This includes: identical or near-identical requirement names, duplicate behavioral descriptions, redefinition of concepts that have their own specs.
- **ecosystem-fit**: Phase 2 MUST check whether existing recipes should reference the new content (backlinks), whether new terminology conflicts with established terms, and whether relevant guidelines are referenced.
- **refactoring-proposal**: When overlap or scope issues are found, Phase 2 MUST produce a concrete refactoring proposal specifying exact changes: which requirements to move, merge, or split, and which files are affected.
- **granular-assessment**: Refactoring proposals MUST be per-requirement/section, not per-recipe. A recipe with 10 parts where 2 are valuable MUST have a proposal that extracts those 2.

## Appearance

Not applicable — this phase is an automated analysis with no visual UI; its output is a GitHub PR review rendered by GitHub.

## States

| State | Behavior |
|-------|----------|
| Analyzing | Placement, granularity, overlap, and ecosystem checks are running |
| Proposing | Issues were found and a refactoring proposal is being produced |
| Approved | No scope issues; a PR review with Approve is posted |
| Rejected | Scope issues found; a Request Changes review with the refactoring proposal is posted |

## Accessibility

Not applicable — the phase interacts through GitHub's PR interface, which provides its own accessible rendering of bot comments.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pr-scope-001 | placement-analysis | A recipe placed in `guidelines/` with a recipe-type domain | Flagged as incorrect placement |
| pr-scope-002 | granularity-check | A recipe with 18 MUST requirements | Flagged as potentially too broad |
| pr-scope-003 | granularity-check | A recipe with 2 requirements | Flagged as potentially too narrow |
| pr-scope-004 | overlap-detection | A recipe whose requirement names duplicate an existing recipe's | Overlap flagged with the matching file named |
| pr-scope-005 | ecosystem-fit | A new recipe that no existing related recipe links to | Backlink candidates are listed |
| pr-scope-006 | refactoring-proposal, granular-assessment | A recipe with 10 parts of which 2 are novel | The proposal extracts exactly those 2 parts, per requirement |

## Edge Cases

- **Modification-only PR**: Overlap detection skips unchanged sections but still checks that modifications do not introduce new overlap.
- **Non-recipe files**: This phase does not run for guidelines or principles; scoping and refactoring are recipe-specific.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| Max MUST requirements | integer | 15 | Above this a recipe is flagged as potentially too broad |
| Max states | integer | 8 | Above this a recipe is flagged as potentially too broad |
| Min requirements | integer | 3 | Below this a recipe is flagged as potentially too narrow |
| Model | string | Claude Opus | Overlap and scoping require strong reasoning |

## Logging

This ingredient defines no events of its own; the pipeline-level `Pipeline` events (phase completed, short-circuited) cover it.

## Platform Notes

- **macOS (OpenClaw)**: Runs on the OpenClaw host with read access to a full checkout of the cookbook so overlap detection can search all content.
- **SwiftUI / Compose / React/Web**: Not applicable — this is an automation phase with no UI framework.

## Design Decisions

**Decision**: Proposals are per requirement or section, never per whole recipe.
**Rationale**: A contribution often mixes valuable and redundant parts; a whole-recipe accept/reject discards the valuable part, so the phase proposes extraction of just the parts worth keeping.
**Approved**: yes

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [separation-of-concerns](agenticdevelopercookbook://compliance/best-practices#separation-of-concerns) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the PR Review Pipeline recipe |

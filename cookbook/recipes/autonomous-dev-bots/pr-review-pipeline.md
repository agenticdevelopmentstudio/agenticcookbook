---
id: c3f7a9e2-1b5d-4c8e-a2d6-9e4f1c3b7a5d
title: "PR Review Pipeline"
domain: agenticdevelopercookbook://recipes/autonomous-dev-bots/pr-review-pipeline
type: recipe
version: 1.0.0
status: wip
language: en
created: 2026-03-28
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Three-phase automated review pipeline for cookbook contributions — review, refactoring, evaluate — running on OpenClaw with GitHub App bot personas."
platforms:
  - macos
tags:
  - automation
  - review
  - ci
  - github
ingredients:
  - agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-review-phase
  - agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-scope-phase
  - agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-evaluate-phase
  - agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-fix-agent
depends-on: []
related:
  - agenticdevelopercookbook://workflows/code-review
  - agenticdevelopercookbook://compliance/best-practices
references:
  - https://docs.github.com/en/rest/checks/runs
  - https://docs.github.com/en/apps/creating-github-apps
  - https://vale.sh
  - https://github.com/DavidAnson/markdownlint-cli2
  - https://docs.openclaw.ai
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# PR Review Pipeline

## Overview

An autonomous dev bot that reviews pull requests to the Agentic Developer Cookbook. Three sequential phases — Review, Refactoring & Scoping, Evaluate — each run by a distinct GitHub App bot persona. The pipeline runs on OpenClaw, triggered by GitHub webhooks, and posts structured PR reviews that gate merging.

When a contributor submits a PR to the cookbook (via `/contribute-to-cookbook` or manually), this pipeline runs automatically:

1. **Phase 1: Review** — structural validation, prose quality, content completeness, convention compliance. Fixes what it can (up to 3 iterations), rejects what it cannot.
2. **Phase 2: Refactoring & Scoping** — placement analysis, granularity assessment, overlap detection against all cookbook content, refactoring proposals.
3. **Phase 3: Evaluate** — value scoring, risk assessment, ecosystem research, recommendation to human reviewer.

Phases run **sequentially**. If a phase rejects, subsequent phases do not run. Each phase posts a GitHub PR review (Approve or Request Changes) under its own bot identity.

The PR is unmergeable until all three phase bots approve AND a human reviewer approves.

The recipe composes four ingredients: one per phase, plus the fix agent that applies automated fixes. The trigger, sequencing, rejection and appeal behavior, and the execution platform belong to the recipe because they span the ingredients.

### Pipeline Outcomes

| Outcome | Description | Next action |
|---------|-------------|-------------|
| Accept | Passes all phases, high value | Human reviewer approves, PR is mergeable |
| Accept with refactoring | Has value, needs structural changes | Refactoring agent applies changes, pipeline reruns |
| Partial accept | Some parts valuable, others not | Proposal extracts good parts, rejects rest. Human decides. |
| Reject | No parts meet the bar | Detailed per-section rationale posted. Contributor can appeal. |
| Reject with appeal | Contributor disputes rejection | Human reviewer evaluates the appeal |

### GitHub Apps

Four GitHub App identities are required:

| App | Purpose | Posts as |
|-----|---------|---------|
| Cookbook Review Bot | Phase 1: structural, prose, completeness, conventions | `@cookbook-review-bot[bot]` |
| Cookbook Scope Bot | Phase 2: placement, granularity, overlap, ecosystem fit | `@cookbook-scope-bot[bot]` |
| Cookbook Eval Bot | Phase 3: value, risk, recommendation | `@cookbook-eval-bot[bot]` |
| Cookbook Fix Bot | Refactoring agent: applies all automated fixes | `@cookbook-fix-bot[bot]` |

Each app requires:
- `checks:write` permission (to create check runs)
- `pull_requests:write` permission (to post reviews and suggested changes)
- `contents:write` permission (Fix Bot only — to push commits)
- Private key PEM stored on the execution Mac
- Installation tokens generated per run via `gh-token` extension

### Execution Platform

#### OpenClaw Configuration

- **Trigger**: GitHub webhook configured to POST `pull_request` events to `http://<mac-ip>:18789/hooks/agent`
- **Fallback**: OpenClaw cron job polling `gh pr list --repo agenticdevelopercookbook/cookbook --state open` every 5 minutes
- **Session**: Isolated session per PR review run
- **Model**: Claude Opus for Phase 2 (overlap/scoping requires strong reasoning) and Phase 3 (evaluation). Sonnet for Phase 1 (structural checks are more mechanical).
- **Timeout**: 48 hours max per run
- **Tools**: Shell access to `gh`, `git`, `vale`, `markdownlint-cli2`

#### Conversational Control

The pipeline is controllable via chat (any connected channel — Slack, Discord, iMessage):

- "What's the status of PR #42?" → shows current phase, findings so far
- "Re-run review on PR #42" → triggers a fresh pipeline run
- "Show open PRs waiting for my review" → lists PRs that passed all phases and need human approval
- "Approve refactoring on PR #42" → human approves the refactoring proposal, triggers refactoring agent

#### External Tools

| Tool | Purpose | Installation |
|------|---------|-------------|
| `gh` | GitHub CLI for PR operations, reviews, comments | `brew install gh` |
| `vale` | Prose linting with custom Cookbook style | `brew install vale` |
| `markdownlint-cli2` | Structural markdown linting | `npm install -g markdownlint-cli2` |
| `gh-token` | GitHub App installation token generation | `gh extension install Link-/gh-token` |

### Logging

Subsystem: `pr-review-pipeline` | Category: `Pipeline`

Pipeline-level events are listed here. The fix iteration event is in the PR review phase ingredient and the fix bot commit event is in the PR fix agent ingredient.

| Event | Level | Message |
|-------|-------|---------|
| Pipeline started | info | `Pipeline: started for PR #{{pr_number}} on {{repo}}` |
| Phase completed | info | `Pipeline: phase {{phase}} completed — {{result}}` |
| Phase short-circuited | info | `Pipeline: skipping phase {{phase}} — prior phase rejected` |
| Fix bot committed | info | `Pipeline: fix bot pushed commit {{sha}} for PR #{{pr_number}}` |
| Rate limit hit | warning | `Pipeline: GitHub API rate limited — retrying in {{seconds}}s` |
| Pipeline failed | error | `Pipeline: failed for PR #{{pr_number}} — {{error}}` |

### Sections that do not apply

The original recipe recorded Appearance, States, and Accessibility as not applicable because the pipeline is automated with no visual UI: its state is tracked through GitHub PR status checks and bot comments, and it interacts through GitHub's PR interface, whose accessible rendering of plain-markdown bot comments is inherited. Each ingredient states this in its own Appearance, States, and Accessibility sections.

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| PR review phase | `agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-review-phase` | Phase 1: structural validation, markdownlint, Vale prose style, LLM clarity pass, completeness, conventions, bounded fix loop | Yes | Max fix iterations (3); Claude Sonnet |
| PR scope phase | `agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-scope-phase` | Phase 2: placement, granularity, overlap detection, ecosystem fit, per-requirement refactoring proposals | Yes | Granularity thresholds (15 MUST requirements, 8 states, 3 requirements); Claude Opus |
| PR evaluate phase | `agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-evaluate-phase` | Phase 3: value and risk scoring, external research, recommendation to the human reviewer | Yes | Claude Opus |
| PR fix agent | `agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-fix-agent` | The single identity that applies automated fixes by commit or suggested change per the contributor's preference | Yes | `fix-preference` (`auto` default or `review`) stored in the PR body |

## Integration Requirements

### Trigger and execution

- **webhook-trigger**: The pipeline MUST trigger when a GitHub `pull_request` event (opened, synchronize, reopened) is received at the OpenClaw webhook endpoint (`POST /hooks/agent`).
- **poll-fallback**: The pipeline SHOULD fall back to polling via `gh pr list` on a cron schedule if webhooks are unavailable.
- **isolated-session**: Each pipeline run MUST execute in an isolated OpenClaw agent session to prevent cross-contamination between PR reviews.
- **sequential-phases**: Phases MUST run sequentially: Phase 1 → Phase 2 → Phase 3.
- **short-circuit**: The pipeline MUST stop and not run subsequent phases if a phase posts "Request Changes".
- **rerun-on-update**: The pipeline MUST rerun from Phase 1 when new commits are pushed to the PR branch.

### Rejection and appeal

- **rejection-format**: A rejecting phase MUST post a PR review with "Request Changes" status, including per-issue explanation of what failed and why.
- **branch-protection**: The repository MUST be configured to require approval from all three phase bot GitHub Apps plus a human reviewer before merging is allowed.
- **appeal-process**: If a contributor replies to a rejection comment disputing the decision, the pipeline MUST flag the PR for human review rather than re-running automatically.
- **rerun-after-fix**: After the refactoring agent applies fixes, the pipeline MUST rerun from Phase 1 on the updated content.

### Cross-ingredient wiring

- **phase-findings-flow-forward**: Phase 2 MUST receive the cleaned content and findings from Phase 1, and Phase 3 MUST receive the findings of both prior phases, since Phase 3's quality score depends on how clean the Phase 1 and Phase 2 passes were.
- **fixes-come-from-fix-agent**: Every automated change, whether a Phase 1 structural fix or a human-approved Phase 2 refactoring proposal, MUST be applied by the PR fix agent, and the three phase bots MUST remain read-only reviewers.
- **fix-preference-read-at-fix-time**: The fix agent MUST read the contributor's stored fix preference from the PR body on each run and MUST NOT cache it across PRs.

## Layout

This is a non-UI recipe: the layout is the pipeline arrangement and the identity each stage posts under.

```
 GitHub PR event ──▶ OpenClaw webhook (or cron poll fallback)
                          │ isolated session per run
                          ▼
   ┌────────────────┐  approve   ┌────────────────┐  approve   ┌────────────────┐
   │ Phase 1 Review │ ─────────▶ │ Phase 2 Scope  │ ─────────▶ │ Phase 3 Eval   │
   │ review-bot     │            │ scope-bot      │            │ eval-bot       │
   └───────┬────────┘            └───────┬────────┘            └───────┬────────┘
           │ Request Changes             │ Request Changes             │ recommendation
           ▼ (later phases skipped)      ▼                             ▼
   ┌─────────────────────────────────────────────────┐        human reviewer decides
   │ PR fix agent (fix-bot): commit or suggest        │ ── pushes → pipeline reruns from Phase 1
   └─────────────────────────────────────────────────┘
```

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| Fix preference | Contributor via `/contribute-to-cookbook` | PR fix agent | one-way | HTML comment in the PR body: `<!-- fix-preference: auto -->` or `<!-- fix-preference: review -->`; default `auto` |
| Phase result (approve or request changes) | Each phase bot | The next phase, branch protection, the human reviewer | one-way | GitHub PR review under the phase bot's identity |
| Phase findings | Phase 1 and Phase 2 | Phase 3 and the fix agent | one-way | Findings carried within the isolated session run and summarized in the PR review |
| Refactoring proposal | Phase 2 | Human reviewer, then the fix agent | one-way | Posted in the Phase 2 review; applied only after the human approves it |
| Rejection and appeal thread | Rejecting phase and contributor | Pipeline and human reviewer | two-way | PR review comments; a contributor reply disputing the decision flags the PR for human review |
| Commit SHA under review | PR branch | All phases | one-way | A new push cancels the current run and restarts from Phase 1 on the latest commit |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| prp-001 | structural-validation, rejection-format | PR adding a recipe with missing `id` field | Phase 1 rejects, posts review requesting fix |
| prp-002 | overlap-detection, rejection-format | PR adding a recipe with requirements duplicating an existing recipe | Phase 2 flags overlap, suggests consolidation |
| prp-003 | ecosystem-fit, phase-findings-flow-forward | PR modifying a recipe domain without updating references | Phase 3 detects broken cross-references |
| prp-004 | short-circuit, sequential-phases | PR failing Phase 1 | Phase 2 and 3 do not run |
| prp-005 | fix-preference-honored, fixes-come-from-fix-agent | PR with auto-fix enabled, fixable Phase 1 issue | Fix bot pushes corrected commit |
| prp-006 | rerun-on-update, rerun-after-fix | Fix bot pushes a commit to the PR branch | The pipeline restarts from Phase 1 on the new commit |
| prp-007 | appeal-process | Contributor replies to a rejection disputing it | The PR is flagged for human review and no automatic rerun happens |
| prp-008 | branch-protection | All three phase bots approve, no human has approved | Merge is blocked until a human reviewer approves |

The `Requirements` column of prp-003 originally named `cross-reference-integrity`, prp-001 named `recipe-validation, frontmatter-check`, prp-002 named `overlap-detection`, prp-004 named `short-circuit-rejection`, and prp-005 named `auto-fix-preference`; these are the earlier labels for the named requirements now listed above.

## Edge Cases

- **PR with multiple recipes**: run the pipeline once per changed recipe file, aggregate results into a single review per phase
- **PR modifying existing content only**: skip Phase 2 overlap detection for sections that didn't change; still check that modifications don't introduce new overlap
- **PR touching non-recipe files** (guidelines, principles): run Phase 1 and Phase 3 only; skip Phase 2 (scoping/refactoring is recipe-specific)
- **Contributor pushes during pipeline run**: cancel current run, restart from Phase 1 on the latest commit
- **GitHub App rate limits**: implement exponential backoff; if rate-limited during review posting, retry up to 3 times then log failure
- **OpenClaw goes offline**: GitHub webhook delivery retries for up to 8 hours; pending PRs will be picked up by the cron fallback when the Mac comes back online

## Platform Notes

- **macOS (OpenClaw)**: This pipeline runs on macOS via OpenClaw. It is not platform-portable — it depends on OpenClaw's daemon infrastructure, GitHub App webhooks, and Claude Code CLI availability on the host Mac.
- **SwiftUI / Compose / React/Web**: Not applicable — the pipeline is an automation with no UI framework; all interaction is through GitHub's PR interface and chat.

## Design Decisions

**Decision**: Use OpenClaw as the execution platform rather than GitHub Actions or a standalone launchd script.
**Rationale**: OpenClaw is already installed on the execution Mac, provides daemon infrastructure (cron, webhooks, sessions), Claude integration, and conversational control. Avoids building custom daemon management.
**Approved**: yes

**Decision**: Four GitHub Apps (3 phase bots + 1 fix bot) rather than a single bot or GitHub Actions identity.
**Rationale**: Distinct bot personas make PR reviews visually clear — each phase appears as a different reviewer. The fix bot is separate because it writes code while the phase bots are read-only reviewers.
**Approved**: yes

**Decision**: Sequential phase execution (1 → 2 → 3) with short-circuit on rejection.
**Rationale**: Phase 1 fixes content before Phase 2 analyzes it (better to compare clean content). Phase 3 needs findings from both prior phases. Running all phases on content that fails basic structural checks wastes resources.
**Approved**: yes

**Decision**: Contributor can appeal rejections by commenting on the PR.
**Rationale**: Automated review can be wrong. A simple appeal process (comment → human reviews) prevents valid contributions from being permanently blocked by false positives.
**Approved**: yes

**Decision**: LLM readability over human readability (no Flesch-Kincaid), and fix preference asked before PR submission with a default of auto-fix.
**Rationale**: These two decisions apply to a single ingredient each and are recorded in full in the PR review phase ingredient (LLM readability) and the PR fix agent ingredient (fix preference).
**Approved**: yes

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [code-linting](agenticdevelopercookbook://compliance/best-practices#code-linting) | partial | Best Practices |
| [post-generation-verification](agenticdevelopercookbook://compliance/best-practices#post-generation-verification) | partial | Best Practices |
| [safe-defaults](agenticdevelopercookbook://compliance/user-safety#safe-defaults) | partial | User Safety |

> Status is `partial`: this recipe specifies the integration-level requirements that satisfy these checks, but compliance is verified per concrete pipeline deployment, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Restructure into recipe shape; extract component behavior into ingredients |
| 0.1.0 | 2026-03-28 | Mike Fullerton | Initial recipe — captures all design decisions from planning session |

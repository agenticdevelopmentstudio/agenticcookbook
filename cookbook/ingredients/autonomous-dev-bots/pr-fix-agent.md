---
id: FE3522F2-1B94-494E-8136-C8A5EEA876CF
title: "PR Fix Agent"
domain: agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-fix-agent
type: ingredient
version: 1.0.0
status: wip
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Dedicated refactoring agent identity that applies automated fixes by commit or suggested change according to the contributor's stored fix preference"
platforms:
  - macos
tags:
  - automation
  - review
  - github
  - fix-bot
depends-on: []
related:
  - agenticdevelopercookbook://recipes/autonomous-dev-bots/pr-review-pipeline
  - agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-review-phase
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# PR Fix Agent

## Overview

The PR fix agent is the Cookbook Fix Bot (`@cookbook-fix-bot[bot]`): the single identity that writes to a contribution during the pipeline. It applies structural fixes from Phase 1 and refactoring proposals approved by the human reviewer from Phase 2, either committing directly or posting GitHub suggested changes, according to a preference the contributor states before submitting the PR. The three phase bots stay read-only reviewers.

### Contributor Preference

The `/contribute-to-cookbook` skill asks the contributor before PR submission whether fixes should be applied automatically or reviewed one by one, and records the answer in the PR body as an HTML comment (`<!-- fix-preference: auto -->` or `<!-- fix-preference: review -->`).

## Behavioral Requirements

### Contributor preferences

- **fix-preference-prompt**: The `/contribute-to-cookbook` skill MUST ask the contributor before PR submission: "If the review pipeline finds fixable issues, would you like us to fix them automatically, or review each change?"
- **fix-preference-default**: The default preference MUST be "fix automatically".
- **fix-preference-storage**: The preference MUST be stored in the PR body as metadata (e.g., `<!-- fix-preference: auto -->` or `<!-- fix-preference: review -->`).
- **fix-preference-honored**: The refactoring agent MUST honor the stored preference — committing directly for "auto", posting suggested changes for "review".

### Refactoring agent

- **dedicated-persona**: All automated fixes and refactoring MUST be applied by a single dedicated refactoring agent with its own GitHub App identity, distinct from the three phase bots.
- **fix-or-suggest**: The refactoring agent MUST commit directly if the contributor chose "fix automatically", or post GitHub suggested changes if the contributor chose "review each change".
- **scope-of-fixes**: The refactoring agent handles fixes from all phases: structural fixes from Phase 1, refactoring proposals approved by the human reviewer from Phase 2.

## Appearance

Not applicable — the agent acts through commits and GitHub suggested changes, rendered by GitHub.

## States

| State | Behavior |
|-------|----------|
| Idle | No fixes pending |
| Committing | Preference is "auto"; fixes are pushed as a commit by the Fix Bot |
| Suggesting | Preference is "review"; fixes are posted as GitHub suggested changes |

## Accessibility

Not applicable — the agent interacts through GitHub's PR interface, which provides its own accessible rendering of commits and suggestions.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pr-fix-001 | fix-preference-default | PR body with no preference metadata | The agent treats the preference as "auto" |
| pr-fix-002 | fix-preference-storage | Contributor chooses "review each change" | PR body contains `<!-- fix-preference: review -->` |
| pr-fix-003 | fix-or-suggest, fix-preference-honored | Preference "auto" and a fixable Phase 1 issue | The Fix Bot pushes a corrected commit |
| pr-fix-004 | fix-or-suggest, fix-preference-honored | Preference "review" and a fixable Phase 1 issue | The Fix Bot posts a suggested change and pushes no commit |
| pr-fix-005 | dedicated-persona | Any automated fix | The author is `@cookbook-fix-bot[bot]`, never a phase bot |
| pr-fix-006 | scope-of-fixes | A Phase 2 refactoring proposal approved by the human reviewer | The Fix Bot applies it |

## Edge Cases

- **Unapproved proposals**: The agent MUST NOT apply a Phase 2 refactoring proposal before the human reviewer approves it.
- **Missing metadata**: A PR body with no preference comment falls back to the default.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `fix-preference` | `auto` or `review` | `auto` | Stored in the PR body; selects commit or suggested-change delivery |
| App permissions | set | `checks:write`, `pull_requests:write`, `contents:write` | The Fix Bot is the only app with `contents:write`, needed to push commits |

## Logging

Subsystem: `pr-review-pipeline` | Category: `Pipeline`

| Event | Level | Message |
|-------|-------|---------|
| Fix bot committed | info | `Pipeline: fix bot pushed commit {{sha}} for PR #{{pr_number}}` |

## Platform Notes

- **macOS (OpenClaw)**: Authenticates as a GitHub App with an installation token generated per run via the `gh-token` extension; the private key PEM is stored on the execution Mac.
- **SwiftUI / Compose / React/Web**: Not applicable — this is an automation agent with no UI framework.

## Design Decisions

**Decision**: Fix preference asked before PR submission, default auto-fix.
**Rationale**: Most contributors want hands-off after submission. Power users who want control can opt into review-each. The choice is per-PR, stored as PR metadata.
**Approved**: yes

**Decision**: The fix bot is a separate GitHub App from the phase bots.
**Rationale**: The fix bot writes code while the phase bots are read-only reviewers, so separating identities keeps write permission (`contents:write`) off the reviewers.
**Approved**: yes

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [atomic-commits](agenticdevelopercookbook://compliance/best-practices#atomic-commits) | partial | Best Practices |
| [safe-defaults](agenticdevelopercookbook://compliance/user-safety#safe-defaults) | partial | User Safety |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the PR Review Pipeline recipe |

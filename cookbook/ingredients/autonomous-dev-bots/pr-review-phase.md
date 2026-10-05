---
id: 32EB5FA7-31BA-49D2-8223-A530D8CC7092
title: "PR Review Phase"
domain: agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-review-phase
type: ingredient
version: 1.0.0
status: wip
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Phase 1 of the PR review pipeline: structural validation, markdownlint, Vale prose style, LLM clarity pass, completeness and convention checks with a bounded fix loop"
platforms:
  - macos
tags:
  - automation
  - review
  - ci
  - github
  - vale
  - markdownlint
depends-on: []
related:
  - agenticdevelopercookbook://recipes/autonomous-dev-bots/pr-review-pipeline
  - agenticdevelopercookbook://ingredients/autonomous-dev-bots/pr-fix-agent
references:
  - https://vale.sh
  - https://github.com/DavidAnson/markdownlint-cli2
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# PR Review Phase

## Overview

The PR review phase is Phase 1 of the cookbook PR review pipeline, run by the Cookbook Review Bot (`@cookbook-review-bot[bot]`). It checks a contributed artifact for structural validity, prose quality, content completeness, and convention compliance, fixes what it can in a bounded loop, and rejects what it cannot. It reads the PR content and posts a GitHub PR review (Approve or Request Changes).

### Custom Vale Style: Cookbook

A custom Vale style (`vale/styles/Cookbook/`) with rules optimized for LLM readability:

| Rule | What it flags |
|------|---------------|
| `VagueTerms.yml` | "appropriate", "suitable", "reasonable", "as needed", "standard", "proper", "adequate" |
| `AmbiguousQuantifiers.yml` | "some", "most", "usually", "often", "sometimes", "generally", "typically", "normally" |
| `Hedging.yml` | "might want to", "consider using", "it may be helpful", "you could", "perhaps", "arguably" |
| `ImplicitReferences.yml` | "as mentioned above", "the usual approach", "handle this correctly", "see above", "as before" |
| `CasualRFC2119.yml` | Lowercase "must", "should", "shall" in requirement sections that are not bolded RFC 2119 keywords |
| `DoubleNegatives.yml` | "must not fail to", "should not avoid", "do not prevent" |
| `AmbiguousPronouns.yml` | "it should", "this must", "that will" at sentence start without clear antecedent in requirement sections |

### LLM Clarity Pass

Beyond Vale's deterministic rules, the LLM clarity pass checks for:

- **Ambiguous antecedents**: pronouns whose referent requires re-reading prior context
- **Implicit assumptions**: statements that assume knowledge not present in the document
- **Terminology drift**: a concept called X in one section and Y in another
- **Section isolation**: can each section be understood without reading the others?
- **Unresolved references**: mentions of concepts not defined or linked
- **Vague quantification in requirements**: "handle multiple items" (how many?) vs "handle 1-1000 items"

## Behavioral Requirements

- **structural-validation**: Phase 1 MUST run all applicable checks from `/validate-cookbook` (frontmatter integrity, content structure, cross-references, indexes, file placement).
- **markdownlint**: Phase 1 MUST run markdownlint-cli2 and auto-fix fixable issues.
- **vale-cookbook-style**: Phase 1 MUST run Vale with the custom Cookbook style checking for: vague terms, ambiguous quantifiers, hedging, implicit references, casual RFC 2119 keywords, double negatives, ambiguous pronouns.
- **llm-clarity-pass**: Phase 1 MUST run an LLM-based clarity analysis checking for: ambiguous antecedents, implicit assumptions, terminology inconsistency across sections, self-containment of sections, unresolved references.
- **content-completeness**: Phase 1 MUST verify all required sections are present and non-empty (or explicitly N/A with reason), MUST requirements have test vectors, appearance values are concrete, logging messages are exact strings, platform notes cover all declared platforms.
- **convention-compliance**: Phase 1 MUST verify named requirements use kebab-case, RFC 2119 keywords are used correctly, domain identifiers match file paths, template variables are used where appropriate.
- **fix-loop**: Phase 1 MUST attempt to fix issues in a loop, max 3 iterations. Each iteration: fix auto-fixable issues (markdownlint, frontmatter), attempt LLM fixes (prose rewrites, inferrable values), re-validate. After 3 iterations, remaining issues are flagged as unfixable.
- **fix-categorization**: Each issue MUST be categorized as: auto-fixable (deterministic tool fix), LLM-fixable (LLM can infer the correction), or human-required (needs contributor or reviewer decision).

## Appearance

Not applicable — this phase is an automated check with no visual UI; its output is a GitHub PR review rendered by GitHub.

## States

| State | Behavior |
|-------|----------|
| Validating | Deterministic checks (structure, markdownlint, Vale) are running |
| Fixing | A fix-loop iteration is applying auto-fixable and LLM-fixable corrections |
| Approved | No unfixed issues remain; a PR review with Approve is posted |
| Rejected | Unfixable or human-required issues remain after 3 iterations; a Request Changes review is posted |

## Accessibility

Not applicable — the phase interacts through GitHub's PR interface. Bot-posted review comments use plain markdown, inheriting GitHub's accessible rendering.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pr-review-001 | structural-validation | PR adding an artifact with a missing `id` field | Phase 1 reports a frontmatter failure and posts a Request Changes review |
| pr-review-002 | markdownlint | PR with a markdownlint-fixable list-indent violation | The violation is auto-fixed and the re-validation passes |
| pr-review-003 | vale-cookbook-style | Requirement text containing "should probably handle as needed" | Vale flags the hedging and vague-term rules |
| pr-review-004 | fix-loop | An issue that remains after each of 3 iterations | The loop stops at 3 iterations and flags the issue as unfixable |
| pr-review-005 | fix-categorization | One markdownlint error, one inferrable missing value, one design question | Categorized respectively as auto-fixable, LLM-fixable, and human-required |
| pr-review-006 | content-completeness | A MUST requirement with no test vector | The completeness check fails for that requirement |
| pr-review-007 | convention-compliance | A requirement named `REQ_001` | Flagged as not kebab-case |

## Edge Cases

- **Non-recipe files**: Guidelines and principles still get Phase 1 checks against their own type's format.
- **Fix loop oscillation**: If a fix in one iteration reintroduces an issue fixed in a previous one, the loop MUST stop and flag the issue rather than continue to the iteration cap.
- **Tool unavailable**: If `vale` or `markdownlint-cli2` is not installed, the phase MUST fail with a reported error rather than silently skipping the check.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `maxFixIterations` | integer | 3 | Upper bound on fix-loop iterations (fix-loop) |
| Model | string | Claude Sonnet | Structural checks are mechanical, so a lighter model is used |

## Logging

Subsystem: `pr-review-pipeline` | Category: `Pipeline`

| Event | Level | Message |
|-------|-------|---------|
| Fix iteration | debug | `Pipeline: phase 1 fix iteration {{n}} — {{fixed}} fixed, {{remaining}} remaining` |

## Platform Notes

- **macOS (OpenClaw)**: Runs on the OpenClaw host with shell access to `gh`, `git`, `vale`, and `markdownlint-cli2`.
- **SwiftUI / Compose / React/Web**: Not applicable — this is an automation phase with no UI framework.

## Design Decisions

**Decision**: LLM readability over human readability (no Flesch-Kincaid).
**Rationale**: Cookbook content is consumed by LLMs, not casual human readers. LLM readability means: explicit, unambiguous, no hedging, consistent terminology, self-contained sections. Traditional readability metrics penalize the precision that LLMs need.
**Approved**: yes

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [code-linting](agenticdevelopercookbook://compliance/best-practices#code-linting) | partial | Best Practices |
| [post-generation-verification](agenticdevelopercookbook://compliance/best-practices#post-generation-verification) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the PR Review Pipeline recipe |

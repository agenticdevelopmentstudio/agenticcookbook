---
id: 6b29562c-4185-4411-aa66-092206d6bfa5
title: "Guideline Applicability Checklist"
type: workflow
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Shared checklist of 38 guideline concerns for planning and implementation pipelines"
platforms: []
tags: 
  - guideline-checklist
depends-on: []
related: 
  - d991b992-07aa-47b9-9d36-4fd1ca81435f
  - 3d970d6a-2d71-48f3-9f84-69c1d823d6e8
  - 8d52028b-d358-4965-93a1-030fc8405068
  - 17216748-46e9-4e92-af3a-f4deeb843a8d
  - 40d630ea-4d62-4c95-9663-80b033e4adae
  - e446ee3e-b8f2-40e7-b93d-3113e6a95e5d
  - d27c35ab-84f6-4f40-8c29-91630fdc90e7
  - ac616d81-16c2-4f33-9ae4-139d5c24318d
  - 0f0c1da3-1c53-417b-890d-0259d7513c65
  - 775da457-30c7-47de-b179-0fae8a8b779d
  - 57cbdb9d-4cf7-4a39-bdd8-99d28be983ca
  - 6302654b-8200-4e03-862d-4734d4960d19
  - 563aebde-52bf-4011-8907-ecc473fd942c
  - dec7cf4a-449b-47fa-9d6e-f7e9376383a7
  - 29057cf0-a38b-4c35-8b8b-52e12bf54784
  - 3d970d6a-2d71-48f3-9f84-69c1d823d6e8
  - 4cb7c242-3ade-4d59-9c74-67c1d5f9c107
  - 991e72d0-477b-4fd5-bdfa-08680efc0cf9
  - 8075b95b-2678-4893-9a5a-eb77aa9232aa
  - guide/introduction/conventions.md
  - a2b79b0e-7d2c-44f5-b139-abc9cf47d1f5
  - 2aaf1727-aa36-41d1-a660-7dd0456e1d07
  - e114c41c-d203-454c-bc7c-cc128f6ebadd
  - 425271ea-92b6-4df6-9a83-94795f1be377
  - a7ce3621-2fed-478f-8767-b186014c5923
  - ffa8565d-b105-4758-b850-9d9b8119b838
  - 1357be12-5a58-4143-a570-849c114770c5
  - a61b6ede-624b-4424-bdf6-aeb153c9a3ea
  - 793f491f-a352-4478-876d-7c5d871488f7
  - 05d00147-5c49-42d8-bdbd-cf8fd7dc2379
  - db58f79d-1040-4bb2-a862-93ebd390ee12
  - e5af9ba5-f484-40c3-9738-470090f5241c
  - ccffa426-5556-4bbe-8dd6-b43c8e195f64
  - cf05e36f-ea8b-4af2-8df6-c5e772dc25b5
  - 38969d3a-884a-4d6e-adae-5398464ee0de
  - f3ae65a6-f51d-4e42-8f79-fa8097dd3480
  - 8ab7452a-09b8-4f4e-abfc-f7fd700765db
  - 4b60fa16-a4cc-4376-97c3-e455681bffb6
  - f68778f2-65e3-4e89-bbf8-115151efa9dc
references: []
---

# Guideline Applicability Checklist

---
version: 1.1.0
status: draft
created: 2026-03-27
last-updated: 2026-03-27
author: claude-code
copyright: 2026 Mike Fullerton / Temporal
audience: claude-code
scope: [planning, implementation, verification, review]
tags: [checklist, guidelines, cross-reference]
---

## Overview

A shared checklist of all guide.* guidelines that Claude Code MUST evaluate for applicability during a development session. Each workflow recipe (WF-1 through WF-5) references this checklist rather than duplicating it. When guidelines change, only this file needs updating.

During the **Code Planning** phase (WF-2), Claude Code MUST walk through this checklist with the user, asking them to opt in or opt out of each applicable concern. The decisions are recorded and carried forward through implementation (WF-3), verification (WF-4), and review (WF-5).

## Terminology

| Term | Definition |
|------|-----------|
| Opt-in default | The concern is assumed applicable unless the user explicitly opts out |
| Opt-out default | The concern is assumed not applicable unless the user explicitly opts in |
| Ask | Claude Code MUST ask the user — no default assumption |
| Always | The concern is always applicable and cannot be opted out of |

## Checklist

### Core Engineering (Always Apply)

These guidelines are always applicable. Claude Code MUST follow them without asking. They cannot be opted out of.

| File | Guideline | Summary | Workflow Phases |
|------|-----------|---------|-----------------|
| `../agenticdevelopercookbook/cookbook/principles/native-controls.md` | Native controls | Prefer platform built-in frameworks | WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/code-quality/scope-discipline.md` | Surface design decisions | Note and get approval for all behavioral/structural choices | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/concurrency/concurrency.md` | No blocking main thread | All lengthy work on background threads | WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/code-quality/atomic-commits.md` | Small atomic commits | One logical change per commit | WF-1, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/testing/post-generation-verification.md` | Post-generation verification | Build, test, lint, log verify, a11y audit, code review | WF-4 |
| `../agenticdevelopercookbook/cookbook/guidelines/code-quality/linting.md` | Linting from day one | Linter configured, runs on build or pre-commit | WF-3, WF-4 |
| `../agenticdevelopercookbook/cookbook/principles/simplicity.md` | Simplicity | No interleaving of concerns | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/principles/make-it-work-make-it-right-make-it-fast.md` | Work, Right, Fast | Three sequential phases — never skip phase 2 | WF-3 |
| `../agenticdevelopercookbook/cookbook/principles/dependency-injection.md` | Dependency injection | Receive dependencies from outside | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/principles/immutability-by-default.md` | Immutability by default | Default to immutable values | WF-3 |
| `../agenticdevelopercookbook/cookbook/principles/fail-fast.md` | Fail fast | Detect invalid state at point of origin | WF-3 |
| `../agenticdevelopercookbook/cookbook/principles/design-for-deletion.md` | Design for deletion | Build disposable, not reusable | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/principles/yagni.md` | YAGNI | Build for today's known requirements | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/principles/explicit-over-implicit.md` | Explicit over implicit | Visible dependencies, clear intent | WF-3 |
| `../agenticdevelopercookbook/cookbook/principles/separation-of-concerns.md` | Separation of concerns | One reason to change per module | WF-2, WF-3 |

### Testing (Always Apply)

Testing guidelines are always applicable when writing code. The scope and depth may vary based on the task.

| File | Guideline | Summary | Workflow Phases |
|------|-----------|---------|-----------------|
| `../agenticdevelopercookbook/cookbook/guidelines/testing/testing.md` | Comprehensive unit testing | Prioritize unit tests, test state transitions and edge cases | WF-3, WF-4 |
| `../agenticdevelopercookbook/cookbook/guidelines/testing/test-pyramid.md` | Test pyramid | 80% unit / 15% integration / 5% E2E | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/testing/properties-of-good-tests.md` | Properties of good tests | Isolated, deterministic, fast, behavioral, readable | WF-3, WF-4 |
| `../agenticdevelopercookbook/cookbook/guidelines/testing/unit-test-patterns.md` | Unit test patterns | Arrange-Act-Assert, one concept per test | WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/testing/flaky-test-prevention.md` | Flaky test prevention | No shared state, no timing, no real network in unit tests | WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/testing/test-data.md` | Test data | Builder pattern, no magic fixtures | WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/testing/the-testing-workflow.md` | Testing workflow | Write tests alongside code, validate with mutation testing | WF-3, WF-4 |

### Opt-In Concerns (Ask the User)

These concerns apply to many but not all features. Claude Code MUST ask the user about each one during planning. The "Default" column indicates the starting assumption, but the user's answer overrides it.

| File | Guideline | Summary | Default | Prompt Template | Workflow Phases |
|------|-----------|---------|---------|-----------------|-----------------|
| `../agenticdevelopercookbook/cookbook/guidelines/ui/always-show-progress.md` | Show progress | Determinate or indeterminate progress for async work | Opt-in | "Does this feature involve async operations that need progress indication?" | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/observability/logging.md` | Instrumented logging | Structured logging for all components and flows | Opt-in | "This feature will include structured logging. Any components that should be excluded?" | WF-2, WF-3, WF-4 |
| `../agenticdevelopercookbook/cookbook/guidelines/platform/deep-linking.md` | Deep linking | All significant views must be deep linkable | Ask | "Should the views in this feature be deep linkable?" | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/platform/shortcuts-and-automation.md` | Scriptable/automatable | Components scriptable via platform mechanisms | Opt-out | "Does this feature need scripting/automation support (Shortcuts, intents)?" | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/accessibility/accessibility.md` | Accessibility | Platform accessibility APIs from day one | Opt-in | "This feature will include full accessibility support. Any constraints?" | WF-2, WF-3, WF-4 |
| `../agenticdevelopercookbook/cookbook/guidelines/internationalization/localization.md` | Localizability | All user-facing strings localizable | Opt-in | "This feature will use localized strings. Confirm or opt out." | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/internationalization/rtl-support.md` | RTL layout | Support right-to-left languages | Opt-in | "This feature will support RTL layouts. Confirm or opt out." | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/accessibility/accessibility.md` | Accessibility display options | Respond to reduced motion, high contrast, etc. | Opt-in | "This feature will respect accessibility display options. Confirm or opt out." | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/security/privacy.md` | Privacy/security | Data minimization, secure storage, no PII logging | Opt-in | "Does this feature collect, store, or transmit user data?" | WF-2, WF-3, WF-5 |
| `../agenticdevelopercookbook/cookbook/guidelines/feature-management/feature-flags.md` | Feature flags | All features gated behind feature flags | Opt-in | "This feature will be gated behind a feature flag. Confirm or opt out." | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/observability/analytics.md` | Analytics | Significant user actions instrumented | Ask | "Which user actions in this feature should be tracked for analytics?" | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/feature-management/ab-testing.md` | A/B testing | Variant assignment support | Opt-out | "Does this feature need A/B testing / experimentation support?" | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/feature-management/debug-mode.md` | Debug mode | Debug panel entries for flags, analytics, experiments | Opt-in | "This feature will include debug panel entries. Confirm or opt out." | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/testing/property-based-testing.md` | Property-based testing | For parsers, serializers, data transformers | Ask | "Does this feature include data transformations that would benefit from property-based testing?" | WF-2, WF-3 |
| `../agenticdevelopercookbook/cookbook/guidelines/testing/mutation-testing.md` | Mutation testing | Validate tests catch bugs | Ask | "Should we run mutation testing to validate test quality?" | WF-4 |
| `../agenticdevelopercookbook/cookbook/guidelines/testing/security-testing.md` | Security testing | SAST, dependency scanning | Ask | "Should we run security scans (Semgrep, dependency audit)?" | WF-4 |
| `../agenticdevelopercookbook/cookbook/guidelines/implementing/data/database.md` | Database | Schema design, performance, sync, PRAGMA settings | Ask | "Does this feature use a database? The database guideline covers schema design, performance, sync, and operations." | WF-2, WF-3 |

## How to Use This Checklist

### During Code Planning (WF-2)

1. Claude Code reads this checklist
2. For each "Always" item: note it as applicable without asking
3. For each "Opt-in" item: inform the user it will be included, ask for confirmation or opt-out
4. For each "Opt-out" item: ask the user if they want to opt in
5. For each "Ask" item: ask the user the prompt template question
6. Record all decisions in the plan document

### During Code Implementation (WF-3)

1. Apply all "Always" items automatically
2. Apply all opted-in items from the planning phase
3. Skip all opted-out items
4. If a new concern surfaces during implementation, ask the user before proceeding

### During Code Verification (WF-4)

1. Verify all "Always" items are correctly implemented
2. Verify all opted-in items are correctly implemented
3. Confirm opted-out items were not accidentally included
4. Run applicable testing tools (mutation testing, security scanning) based on opt-in decisions

### During Code Review (WF-5)

1. Review against all applicable guidelines
2. Flag any opted-in items that appear missing or incomplete
3. Flag any guideline violations in "Always" items

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-27 | Initial checklist |
| 1.1.0 | 2026-03-29 | Replace domain URLs with file paths |

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
| 1.1.0 | 2026-03-29 | Mike Fullerton | Replace domain URLs with file paths for pipeline compatibility |

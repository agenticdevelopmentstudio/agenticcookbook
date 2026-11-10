---
id: 6a98612f-9f43-4903-87e4-40c964801bbc
title: "Code Verification"
type: workflow
version: 1.0.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "version: 1.0.0"
platforms: 
  - csharp
  - ios
  - kotlin
  - python
  - swift
  - typescript
  - web
  - windows
tags: 
  - code-verification
depends-on: []
related: 
  - 3d970d6a-2d71-48f3-9f84-69c1d823d6e8
  - 17216748-46e9-4e92-af3a-f4deeb843a8d
  - 40d630ea-4d62-4c95-9663-80b033e4adae
  - d27c35ab-84f6-4f40-8c29-91630fdc90e7
  - ac616d81-16c2-4f33-9ae4-139d5c24318d
  - 0f0c1da3-1c53-417b-890d-0259d7513c65
  - 775da457-30c7-47de-b179-0fae8a8b779d
  - 57cbdb9d-4cf7-4a39-bdd8-99d28be983ca
  - 563aebde-52bf-4011-8907-ecc473fd942c
  - 563aebde-52bf-4011-8907-ecc473fd942c
  - 563aebde-52bf-4011-8907-ecc473fd942c
  - 563aebde-52bf-4011-8907-ecc473fd942c
  - 563aebde-52bf-4011-8907-ecc473fd942c
  - 563aebde-52bf-4011-8907-ecc473fd942c
  - 29057cf0-a38b-4c35-8b8b-52e12bf54784
  - 3d970d6a-2d71-48f3-9f84-69c1d823d6e8
  - 4cb7c242-3ade-4d59-9c74-67c1d5f9c107
  - db58f79d-1040-4bb2-a862-93ebd390ee12
  - ccffa426-5556-4bbe-8dd6-b43c8e195f64
  - cf05e36f-ea8b-4af2-8df6-c5e772dc25b5
  - f3ae65a6-f51d-4e42-8f79-fa8097dd3480
references: []
---

# Code Verification

---
version: 1.0.0
status: draft
created: 2026-03-27
last-updated: 2026-03-27
author: claude-code
copyright: 2026 Mike Fullerton / Temporal
audience: claude-code
scope: [verification]
tags: [testing, verification, security, quality, validation]
dependencies:
  - workflow/guideline-checklist.md@1.0.0
  - workflow/branching-strategy.md@1.0.0
  - workflow/code-planning.md@1.0.0
  - workflow/code-implementation.md@1.0.0
---

## Overview

Defines the post-implementation validation phase where Claude Code systematically verifies that all code is correct, all guidelines are followed, all tests pass and are meaningful, and the codebase is ready for review. This phase implements the six-step post-generation verification from [adc.guideline.testing.post-generation-verification](cookbook:563aebde-52bf-4011-8907-ecc473fd942c) and extends it with mutation testing, security scanning, and guideline compliance checking.

This phase runs after WF-3 (Code Implementation) and before WF-5 (Code Review).

## Terminology

| Term | Definition |
|------|-----------|
| Verification | Confirming the implementation meets all requirements, guidelines, and quality standards |
| Mutation testing | Modifying source code (mutants) and re-running tests to verify tests actually catch bugs |
| SAST | Static Application Security Testing — analyzing source code for vulnerabilities without running it |
| Surviving mutant | A code mutation that did not cause any test to fail, indicating a test gap |

## Inputs

- **Implemented code**: All code from WF-3, committed and pushed
- **Guideline decisions**: The opt-in/opt-out matrix from WF-2
- **Approved plan**: The plan from WF-2 including test strategy
- **Active worktree**: The worktree and draft PR from WF-1

## Phases

### Phase 1: Build Verification

**Entry criteria**: WF-3 (Code Implementation) complete. All code committed.

- **REQ-001**: Claude Code MUST build the project for all target platforms specified in the plan. The build MUST succeed with zero errors and zero warnings (or only pre-existing warnings).
- **REQ-002**: If the build fails, Claude Code MUST fix the issue and recommit before proceeding. Do not advance with a broken build.
- **REQ-003**: Claude Code MUST verify that all new files are included in the build target (not orphaned files that compile but aren't linked).

**Exit criteria**: Clean build on all target platforms.

### Phase 2: Test Suite Verification

**Entry criteria**: Phase 1 complete. Build passes.

- **REQ-004**: Claude Code MUST run the full test suite — not just the new tests. All tests MUST pass.
- **REQ-005**: If any test fails, Claude Code MUST investigate and fix the issue. Distinguish between:
  - Tests broken by the new code (fix the code or the test, depending on which is wrong)
  - Pre-existing test failures (note them, do not fix them unless they are in scope)
- **REQ-006**: Claude Code MUST verify test coverage of the new code. Every public function/method MUST have at least one test. Every MUST requirement from the plan or spec MUST have a corresponding test.
- **REQ-007**: Claude Code MUST verify that tests are meaningful — not just asserting `true` or testing trivial getters. Tests should verify behavior, not just existence.

**Exit criteria**: All tests pass. New code has meaningful test coverage.

### Phase 3: Lint Verification

**Entry criteria**: Phase 2 complete. Tests pass.

- **REQ-008**: Claude Code MUST run the project's linter on all new and modified files. All lint errors MUST be resolved.
- **REQ-009**: Claude Code MUST run the project's formatter and commit any formatting changes.
- **REQ-010**: If the project does not have a linter configured, Claude Code SHOULD note this in the PR and recommend adding one (per [adc.guideline.implementing.code-quality.linting](cookbook:775da457-30c7-47de-b179-0fae8a8b779d)).

**Exit criteria**: Zero lint errors on new and modified files.

### Phase 4: Log Verification

**Entry criteria**: Phase 3 complete. Lint clean.

- **REQ-011**: If logging was opted in during planning, Claude Code MUST verify that all components and flows include structured logging per [adc.guideline.implementing.observability.logging](cookbook:0f0c1da3-1c53-417b-890d-0259d7513c65)
- **REQ-012**: Claude Code MUST build and run the application (or tests that exercise the new code) and grep the output for expected log messages from the implementation.
- **REQ-013**: If expected log messages are missing, Claude Code MUST investigate and fix the logging.
- **REQ-014**: Claude Code MUST verify that no PII is logged, even at debug level ([adc.guideline.implementing.security.privacy](cookbook:29057cf0-a38b-4c35-8b8b-52e12bf54784)).

**Exit criteria**: All expected log messages verified in output. No PII in logs.

### Phase 5: Accessibility Audit

**Entry criteria**: Phase 4 complete. Logging verified.

- **REQ-015**: If accessibility was opted in during planning, Claude Code MUST verify:
  1. All interactive elements have semantic roles and labels
  2. Tap targets meet minimum sizes (44x44pt iOS, 48x48dp Android, 40x40 epx Windows)
  3. Text contrast meets WCAG AA (4.5:1 text, 3:1 large text)
  4. Focus order follows visual layout
  5. State changes are announced to screen readers
- **REQ-016**: If the project has accessibility testing tools configured (Accessibility Insights, XCTest accessibility), Claude Code MUST run them.
- **REQ-017**: If accessibility was opted out, Claude Code MUST skip this phase entirely — do not add accessibility attributes that weren't requested.

**Exit criteria**: Accessibility audit passes, or phase skipped per opt-out.

### Phase 6: Guideline Compliance Check

**Entry criteria**: Phase 5 complete.

- **REQ-018**: Claude Code MUST review the guideline decisions from WF-2 and verify each opted-in concern is fully implemented:

  | Concern | Verification |
  |---------|-------------|
  | Logging ([adc.guideline.implementing.observability.logging](cookbook:0f0c1da3-1c53-417b-890d-0259d7513c65)) | All components have structured logging |
  | Deep linking ([adc.guideline.implementing.platform-integration.deep-linking](cookbook:d27c35ab-84f6-4f40-8c29-91630fdc90e7)) | URL patterns implemented per spec |
  | Accessibility ([adc.guideline.implementing.accessibility.accessibility](cookbook:3d970d6a-2d71-48f3-9f84-69c1d823d6e8)) | All views accessible (Phase 5) |
  | Localization ([adc.guideline.implementing.internationalization.localization](cookbook:57cbdb9d-4cf7-4a39-bdd8-99d28be983ca)) | All strings use localization APIs |
  | RTL layout ([adc.guideline.implementing.internationalization.rtl-support](cookbook:4cb7c242-3ade-4d59-9c74-67c1d5f9c107)) | Leading/trailing used, not left/right |
  | Feature flags ([adc.guideline.implementing.feature-management.feature-flags](cookbook:ac616d81-16c2-4f33-9ae4-139d5c24318d)) | Feature gated behind flag |
  | Analytics ([adc.guideline.implementing.observability.analytics](cookbook:17216748-46e9-4e92-af3a-f4deeb843a8d)) | Events instrumented per plan |
  | Privacy ([adc.guideline.implementing.security.privacy](cookbook:29057cf0-a38b-4c35-8b8b-52e12bf54784)) | Secure storage, no PII leaks |

- **REQ-019**: Claude Code MUST verify that opted-out concerns were not accidentally implemented. Unused code is a maintenance burden.
- **REQ-020**: Claude Code MUST compile a compliance summary listing each guideline and its status (pass/fail/not-applicable).

**Exit criteria**: Compliance summary complete. All opted-in guidelines pass.

### Phase 7: Advanced Testing (Conditional)

**Entry criteria**: Phase 6 complete. Basic verification passes.

- **REQ-021**: If mutation testing was opted in during planning, Claude Code MUST run the mutation testing tool and analyze surviving mutants:
  1. Run the mutation testing tool for the platform
  2. Review surviving mutants
  3. Write additional tests to kill surviving mutants where the gap is meaningful
  4. Re-run until mutation score is acceptable or all meaningful mutants are killed
- **REQ-022**: If security testing was opted in during planning, Claude Code MUST run:
  1. SAST scan (Semgrep or platform equivalent)
  2. Dependency vulnerability scan (npm audit, pip-audit, etc.)
  3. Fix any critical or high severity findings
  4. Document any accepted risks in the PR
- **REQ-023**: If property-based testing was opted in, Claude Code MUST verify that property tests exist for data transformations and run them.
- **REQ-024**: If none of the advanced testing options were opted in, Claude Code MUST skip this phase.

**Exit criteria**: Advanced testing complete (or skipped). All findings addressed.

### Phase 8: Verification Summary

**Entry criteria**: All previous phases complete.

- **REQ-025**: Claude Code MUST compile a verification summary and post it as a PR comment (per WF-1 REQ-009). The summary MUST include:
  1. Build status (pass/fail, platforms tested)
  2. Test results (total tests, passed, failed, new tests added)
  3. Lint status
  4. Log verification status
  5. Accessibility audit status
  6. Guideline compliance summary
  7. Advanced testing results (if applicable)
  8. Any issues found and how they were resolved

- **REQ-026**: Claude Code MUST commit any changes made during verification (test additions, lint fixes, logging fixes) per WF-1 REQ-005.

**Exit criteria**: Verification summary posted. All changes committed. Ready for code review (WF-5).

## Guideline Cross-Reference

This workflow references the shared [guideline-checklist.md](guideline-checklist.md).

| Phase | Checklist Items | Notes |
|-------|----------------|-------|
| Phase 1 | [adc.guideline.testing.post-generation-verification](cookbook:563aebde-52bf-4011-8907-ecc473fd942c) (Build) | Build all target platforms |
| Phase 2 | [adc.guideline.testing.post-generation-verification](cookbook:563aebde-52bf-4011-8907-ecc473fd942c) (Test), [adc.guideline.testing.testing](cookbook:40d630ea-4d62-4c95-9663-80b033e4adae), [adc.guideline.testing.test-pyramid](cookbook:f3ae65a6-f51d-4e42-8f79-fa8097dd3480) | Full test suite + coverage |
| Phase 3 | [adc.guideline.testing.post-generation-verification](cookbook:563aebde-52bf-4011-8907-ecc473fd942c) (Lint), [adc.guideline.implementing.code-quality.linting](cookbook:775da457-30c7-47de-b179-0fae8a8b779d) | Linter + formatter |
| Phase 4 | [adc.guideline.testing.post-generation-verification](cookbook:563aebde-52bf-4011-8907-ecc473fd942c) (Log verify), [adc.guideline.implementing.observability.logging](cookbook:0f0c1da3-1c53-417b-890d-0259d7513c65), [adc.guideline.implementing.security.privacy](cookbook:29057cf0-a38b-4c35-8b8b-52e12bf54784) | Log messages + no PII |
| Phase 5 | [adc.guideline.testing.post-generation-verification](cookbook:563aebde-52bf-4011-8907-ecc473fd942c) (A11y audit), [adc.guideline.implementing.accessibility.accessibility](cookbook:3d970d6a-2d71-48f3-9f84-69c1d823d6e8), [adc.guideline.implementing.accessibility.accessibility](cookbook:3d970d6a-2d71-48f3-9f84-69c1d823d6e8) | Full accessibility check |
| Phase 6 | All opted-in items | Compliance verification |
| Phase 7 | [adc.guideline.testing.mutation-testing](cookbook:db58f79d-1040-4bb2-a862-93ebd390ee12), [adc.guideline.testing.security-testing](cookbook:cf05e36f-ea8b-4af2-8df6-c5e772dc25b5), [adc.guideline.testing.property-based-testing](cookbook:ccffa426-5556-4bbe-8dd6-b43c8e195f64) | Mutation, security, property testing |

## Conformance Test Vectors

| ID | Requirements | Scenario | Expected |
|----|-------------|----------|----------|
| verify-001 | REQ-001 | Multi-platform project | Build succeeds on all target platforms |
| verify-002 | REQ-002 | Build fails on one platform | Issue fixed, build retried, passes |
| verify-003 | REQ-004 | 200 existing tests + 15 new | All 215 tests pass |
| verify-004 | REQ-005 | Existing test broken by new code | Investigated: code fixed or test updated |
| verify-005 | REQ-006 | New public function without test | Test added before verification completes |
| verify-006 | REQ-007 | Test just asserts `assertTrue(true)` | Flagged as non-meaningful, rewritten |
| verify-007 | REQ-011 | Logging opted in, component missing logs | Logging added, verified in output |
| verify-008 | REQ-014 | Debug log includes email address | PII removed from log message |
| verify-009 | REQ-015 | Button with 30x30pt tap target | Tap target increased to 44x44pt |
| verify-010 | REQ-018 | Feature flags opted in but not implemented | Flag gate added during verification |
| verify-011 | REQ-019 | Analytics opted out but events instrumented | Analytics code removed |
| verify-012 | REQ-021 | Mutation testing opted in, 3 surviving mutants | Additional tests written, mutants killed |
| verify-013 | REQ-022 | npm audit finds high severity vulnerability | Dependency updated, vulnerability resolved |
| verify-014 | REQ-025 | Verification complete | Summary posted as PR comment with all 7 sections |

## Edge Cases

- **No test runner configured**: If the project lacks test infrastructure, this is a verification failure. Note it in the summary and recommend setup (but don't set it up unless it's in the plan scope).
- **Flaky test discovered**: If a test passes intermittently, quarantine it (mark as skipped with a comment explaining why) and file it as a follow-up. Do not let flaky tests block verification.
- **Verification finds a design flaw**: If verification reveals a fundamental issue (e.g., the architecture doesn't support a required behavior), this is a major plan deviation. Return to WF-2 through WF-3 REQ-020.
- **Security scan finds issues in pre-existing code**: Note them in the PR but do not fix them unless they are in scope. Focus on new/modified code.

## Tool Notes

- **Build tools**: `xcodebuild` (Apple), `./gradlew build` (Android), `npm run build` (Web), `dotnet build` (.NET)
- **Test runners**: `swift test` / `xcodebuild test`, `./gradlew test`, `npm test` / `npx vitest`, `dotnet test`
- **Linters**: SwiftLint, ktlint, ESLint, Roslyn Analyzers (see [adc.guideline.implementing.code-quality.linting](cookbook:775da457-30c7-47de-b179-0fae8a8b779d))
- **Mutation testing**: muter (Swift), Pitest (Kotlin), Stryker (TS/JS/.NET), mutmut (Python)
- **Security scanning**: Semgrep (`semgrep scan --config=auto .`), platform-specific dependency scanners
- **gh**: Use `gh pr comment` to post the verification summary

## Design Decisions

**Decision**: Verification phases run sequentially, not in parallel.
**Rationale**: Each phase builds on the previous — there's no point running the lint check if the build is broken, or checking accessibility if tests fail. Sequential execution catches fundamental issues first and avoids wasted effort.
**Approved**: pending

**Decision**: Advanced testing (mutation, security) is conditional on opt-in, not automatic.
**Rationale**: These tools add significant time to the verification process. For small changes or rapid iteration, the overhead may not be justified. The user decides during planning whether the additional confidence is worth the cost.
**Approved**: pending

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-27 | Initial spec |

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

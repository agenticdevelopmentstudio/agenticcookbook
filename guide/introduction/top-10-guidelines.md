---

id: e6834069-95c2-49b9-8054-237ea302653c
title: "Top 10 Guidelines"
domain: agenticdevelopercookbook://introduction/top-10-guidelines
type: reference
version: 1.0.0
status: draft
language: en
created: 2026-04-09
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "The 10 highest-signal guidelines that catch 80% of issues in AI-assisted codebases."
platforms: []
tags:
  - quick-reference
  - getting-started
depends-on: []
related:
  - agenticdevelopercookbook://introduction/trigger-guide
references: []
approved-by: ""
approved-date: ""
---

# Top 10 Guidelines

The 10 highest-signal guidelines for AI-assisted development. These apply universally regardless of platform, catch real issues during code generation, and are actionable without deep domain knowledge.

Load these when you need a lightweight quality gate without the full 140-guideline set.

| # | Guideline | Why it's here |
|---|-----------|--------------|
| 1 | [Test Pyramid](../guidelines/testing/test-pyramid.md) | Prevents test-suite bloat. AI agents over-generate unit tests and under-generate integration tests — this sets the right ratio. |
| 2 | [Input Validation](../guidelines/implementing/security/input-validation.md) | The #1 security issue in generated code. AI rarely adds server-side validation unless explicitly told to. |
| 3 | [Properties of Good Tests](../guidelines/testing/properties-of-good-tests.md) | AI-generated tests are often brittle, testing implementation details instead of behavior. This fixes that. |
| 4 | [Linting before the first PR](../guidelines/implementing/code-quality/linting.md) | Catches style and format drift before it compounds. Especially important when AI generates code in varying styles. |
| 5 | [Logging](../guidelines/implementing/observability/logging.md) | AI agents skip logging unless told. This ensures every component has structured observability from the start. |
| 6 | [Error Responses](../guidelines/implementing/networking/error-responses.md) | Generated code often has incomplete error handling — happy path only, with catch blocks that swallow errors. |
| 7 | [Accessibility](../guidelines/implementing/accessibility/accessibility.md) | Never added by AI unless explicitly required. Missing accessibility is invisible until a user reports it. |
| 8 | [Atomic Commits](../guidelines/shipping/atomic-commits.md) | Keeps AI-generated PRs reviewable. Without this, AI batches unrelated changes into monolithic commits. |
| 9 | [Sensitive Data](../guidelines/implementing/security/sensitive-data.md) | Prevents PII and secrets from leaking into logs, error responses, and analytics events. |
| 10 | [Scope Discipline](../guidelines/implementing/code-quality/scope-discipline.md) | Prevents AI from over-engineering or scope-creeping. Generated code tends to add features that weren't asked for. |

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-09 | Mike Fullerton | Initial creation |

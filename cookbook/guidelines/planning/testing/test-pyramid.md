---
id: a8f9c003-e970-4f28-bb7d-30a23b891b3f
title: "Test Pyramid"
domain: agenticdevelopercookbook://guidelines/planning/testing/test-pyramid
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Projects SHOULD follow the Google SWE Book ratio: **80% unit / 15% integration / 5% E2E**."
platforms: []
tags:
  - test-pyramid
  - testing
depends-on: []
related: []
references:
  - https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
  - https://kentcdodds.com/blog/write-tests
  - https://web.dev/articles/ta-strategies
  - https://www.wiremock.io/post/rethinking-the-testing-pyramid
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - writing-tests
  - pre-pr
---

# Test Pyramid

Projects SHOULD follow the Google SWE Book ratio: **80% unit / 15% integration / 5% E2E**.

- **Unit tests** — fast, isolated, test one behavior. The foundation.
- **Integration tests** — verify components work together. Use real databases, real
  file systems, real HTTP where practical. Slower but higher confidence.
- **E2E tests** — full system from user perspective. Expensive, brittle, SHOULD be used sparingly.
  Reserve for critical user journeys.

If you're unsure what kind of test to write, write a unit test. If the unit test can't
cover the behavior (e.g., database queries, UI rendering), escalate to integration.

## The shape is context-dependent

The pyramid is a default, not dogma. Teams SHOULD choose the test distribution per
system based on where risk actually lives, not a fixed ratio. Integration-heavy systems
(thin logic over many collaborators — databases, queues, external services) MAY instead
fit the "testing trophy" shape: a larger band of integration tests, with static analysis
and type-checking as the broad base beneath them. When most of the risk is in how
components interact rather than in isolated logic, the trophy SHOULD be preferred over
the pyramid.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-06-10 | Mike Fullerton | Cite recovered Tier-1 research sources (adversarially-audited) |
| 1.1.0 | 2026-06-09 | Mike Fullerton | Reframe as context-dependent shape (incl. testing trophy + static analysis) |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

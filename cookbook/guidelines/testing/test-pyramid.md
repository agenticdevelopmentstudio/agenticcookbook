---
id: f3ae65a6-f51d-4e42-8f79-fa8097dd3480
title: "Test Pyramid"
domain: agenticdevelopercookbook://guidelines/testing/test-pyramid
type: guideline
version: 1.1.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-06-09
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
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
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

The classic pyramid (many unit, fewer integration, fewest E2E) is a sensible **default**,
not dogma. Some systems fit a different shape: integration-heavy services, I/O-bound code,
or thin-logic UIs often match the "testing trophy" better — more integration tests, with
static analysis and type-checking forming the broad foundational base. Teams SHOULD pick the
test distribution deliberately, per system, based on where the real risk lives, rather than
forcing a fixed ratio.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-06-09 | Mike Fullerton | Reframe as context-dependent shape (incl. testing trophy + static analysis) |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

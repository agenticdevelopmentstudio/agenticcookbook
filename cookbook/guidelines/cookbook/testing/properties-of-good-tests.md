---
id: d2c1aaaf-3fc7-4410-ab9a-06c264aa3208
title: "Properties of Good Tests"
domain: agenticdevelopercookbook://guidelines/cookbook/testing/properties-of-good-tests
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Properties that test vectors in cookbook artifacts (ingredients, recipes) should exhibit — adapted from Kent Beck's Test Desiderata."
platforms: []
tags:
  - properties-of-good-tests
  - testing
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - writing-tests
  - code-review
---

# Properties of Good Tests

When writing test vectors in cookbook artifacts (ingredients and recipes), each test vector should exhibit these properties — adapted from Kent Beck's Test Desiderata.

## For test vectors in cookbook artifacts

1. **Isolated** — each test vector MUST be independent; no shared mutable state or ordering dependency between vectors
2. **Deterministic** — the expected result MUST be unambiguous; the same input always produces the same output
3. **Behavioral** — test vectors SHOULD verify what the component does, not how it does it internally
4. **Specific** — each vector SHOULD target one behavior or edge case; a failure points to exactly one cause
5. **Readable** — a test vector MUST clearly communicate what it tests and what the expected outcome is
6. **Predictive** — the set of test vectors SHOULD be sufficient to catch real bugs; if all vectors pass, the implementation is likely correct

## Less relevant for cookbook authoring

The remaining Beck desiderata (fast, composable, writable, automated, structure-insensitive, inspiring) apply to the generated test code, not to the test vector specifications in cookbook artifacts. They are covered by the implementing and testing use cases.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for cookbook use case — reframe for test vector authoring |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

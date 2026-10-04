---
id: 59ffd7c7-2bdc-4f7b-b6f3-07d1f24599a3
title: "Unit Test Patterns"
domain: agenticdevelopercookbook://guidelines/cookbook/testing/unit-test-patterns
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "How to write test vectors in cookbook artifacts — use AAA structure, one concept per vector, descriptive names."
platforms: []
tags:
  - testing
  - unit-test-patterns
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - writing-tests
---

# Unit Test Patterns

When writing test vectors in cookbook artifacts (ingredients and recipes), structure them as Arrange-Act-Assert specifications so that code generators produce well-structured test code.

## Test vector structure

Each test vector in a cookbook artifact SHOULD follow the Arrange-Act-Assert pattern:

- **Arrange** — describe the preconditions and input state
- **Act** — describe the action or method call being tested
- **Assert** — describe the expected outcome

## Rules for test vectors

- Each vector MUST test one behavioral concept — not multiple unrelated assertions
- Vectors MUST NOT depend on each other — each is self-contained
- Vectors SHOULD target the public API described in the artifact's requirements, not implementation details

## Naming test vectors

Use descriptive names that read as specifications:
- `test_parse_order_with_valid_json_returns_order`
- `ParseOrder_WithMissingField_ThrowsValidationError`
- `"returns empty list when no results match"`

These names will be used verbatim by code generators, so they MUST be clear enough to serve as test documentation.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for cookbook use case — reframe for test vector authoring |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

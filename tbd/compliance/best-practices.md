---
id: D931B5B1-F54F-46F1-894F-420957C6D2AE
title: "Best Practices Compliance"
type: compliance
version: 1.0.1
status: draft
language: en
created: 2026-03-28
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compliance checks for testing, code quality, error handling, and separation of concerns."
platforms: []
tags: [compliance, best-practices]
depends-on: []
related:
  - tbd/compliance/security.md
  - tbd/compliance/reliability.md
  - tbd/compliance/performance.md
references: []
---

# Best Practices Compliance

Best practices compliance covers the engineering fundamentals that keep codebases healthy and maintainable — testing strategy, code quality, error handling, and architectural separation. These checks apply broadly to any recipe that produces or modifies code.

## Applicability

This category applies to any recipe or guideline that defines, generates, or modifies source code. If a recipe produces implementation artifacts, these checks govern how that code is tested, structured, and maintained.

## Checks

### unit-test-coverage

Business logic MUST have unit tests with meaningful assertions.

**Applies when:** recipe implements business logic or utility functions.

**Guidelines:**
- [adc.guideline.testing.testing](cookbook:40d630ea-4d62-4c95-9663-80b033e4adae)
- [adc.guideline.testing.unit-test-patterns](cookbook:4b60fa16-a4cc-4376-97c3-e455681bffb6)

---

### test-pyramid

Test distribution SHOULD follow the test pyramid (many unit, fewer integration, fewest E2E).

**Applies when:** recipe defines a test strategy or test suite.

**Guidelines:**
- [adc.guideline.testing.test-pyramid](cookbook:f3ae65a6-f51d-4e42-8f79-fa8097dd3480)

---

### atomic-commits

Changes MUST be committed atomically — one logical change per commit.

**Applies when:** recipe describes a development workflow or commit strategy.

**Guidelines:**
- [adc.guideline.implementing.code-quality.atomic-commits](cookbook:8075b95b-2678-4893-9a5a-eb77aa9232aa)

---

### code-linting

Code MUST pass configured linting rules without suppression.

**Applies when:** recipe produces source code in any language.

**Guidelines:**
- [adc.guideline.implementing.code-quality.linting](cookbook:775da457-30c7-47de-b179-0fae8a8b779d)

---

### post-generation-verification

AI-generated code MUST pass build, test, lint, and log verification before acceptance.

**Applies when:** recipe involves AI-assisted code generation.

**Guidelines:**
- [adc.guideline.testing.post-generation-verification](cookbook:563aebde-52bf-4011-8907-ecc473fd942c)

---

### explicit-error-handling

Errors MUST be handled explicitly; MUST NOT be silently swallowed.

**Applies when:** recipe includes error paths, exception handling, or Result/Optional unwrapping.

**Guidelines:**
- [adc.principle.fail-fast](cookbook:425271ea-92b6-4df6-9a83-94795f1be377) (principle)

---

### separation-of-concerns

Business logic MUST be separated from presentation and infrastructure.

**Applies when:** recipe spans multiple architectural layers (UI, domain, data).

**Guidelines:**
- [adc.principle.separation-of-concerns](cookbook:1357be12-5a58-4143-a570-849c114770c5) (principle)

---

### good-test-properties

Tests MUST be fast, isolated, repeatable, and self-validating.

**Applies when:** recipe defines or includes test implementations.

**Guidelines:**
- [adc.guideline.testing.properties-of-good-tests](cookbook:e5af9ba5-f484-40c3-9738-470090f5241c)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |

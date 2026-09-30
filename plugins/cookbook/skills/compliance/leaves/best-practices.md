<!-- leaf: compliance/best-practices · source: compliance/best-practices.md -->

**Rules** (cite as `compliance/best-practices#<slug>`):

- `business-logic-have-unit-tests-meaningful` MUST — Business logic MUST have unit tests with meaningful assertions.
- `test-distribution-follow-test-pyramid-many` SHOULD — Test distribution SHOULD follow the test pyramid (many unit, fewer integration, fewest E2E).
- `changes-committed-atomically-one-logical` MUST — Changes MUST be committed atomically — one logical change per commit.
- `code-pass-configured-linting-rules` MUST — Code MUST pass configured linting rules without suppression.
- `ai-generated-code-pass-build-test-lint` MUST — AI-generated code MUST pass build, test, lint, and log verification before acceptance.
- `errors-handled-explicitly-silently-swallowed` MUST — Errors MUST be handled explicitly; MUST NOT be silently swallowed.
- `business-logic-separated-from-presentation-infrastructure` MUST — Business logic MUST be separated from presentation and infrastructure.
- `tests-fast-isolated-repeatable-self` MUST — Tests MUST be fast, isolated, repeatable, and self-validating.

# Best Practices Compliance

Best practices compliance covers the engineering fundamentals that keep codebases healthy and maintainable — testing strategy, code quality, error handling, and architectural separation. These checks apply broadly to any recipe that produces or modifies code.

## Applicability

This category applies to any recipe or guideline that defines, generates, or modifies source code. If a recipe produces implementation artifacts, these checks govern how that code is tested, structured, and maintained.

## Checks

### unit-test-coverage

Business logic MUST have unit tests with meaningful assertions.

**Applies when:** recipe implements business logic or utility functions.

**Guidelines:**
- Testing
- Unit Test Patterns

---

### test-pyramid

Test distribution SHOULD follow the test pyramid (many unit, fewer integration, fewest E2E).

**Applies when:** recipe defines a test strategy or test suite.

**Guidelines:**
- Test Pyramid

---

### atomic-commits

Changes MUST be committed atomically — one logical change per commit.

**Applies when:** recipe describes a development workflow or commit strategy.

**Guidelines:**
- Atomic Commits

---

### code-linting

Code MUST pass configured linting rules without suppression.

**Applies when:** recipe produces source code in any language.

**Guidelines:**
- Linting

---

### post-generation-verification

AI-generated code MUST pass build, test, lint, and log verification before acceptance.

**Applies when:** recipe involves AI-assisted code generation.

**Guidelines:**
- Post-Generation Verification

---

### explicit-error-handling

Errors MUST be handled explicitly; MUST NOT be silently swallowed.

**Applies when:** recipe includes error paths, exception handling, or Result/Optional unwrapping.

**Guidelines:**
- Fail Fast (principle)

---

### separation-of-concerns

Business logic MUST be separated from presentation and infrastructure.

**Applies when:** recipe spans multiple architectural layers (UI, domain, data).

**Guidelines:**
- Separation of Concerns (principle)

---

### good-test-properties

Tests MUST be fast, isolated, repeatable, and self-validating.

**Applies when:** recipe defines or includes test implementations.

**Guidelines:**
- Properties of Good Tests

<!-- leaf: test-general/test-pyramid · source: guidelines/testing/test-pyramid.md -->

**Rules** (cite as `test-general/test-pyramid#<slug>`):

- `projects-follow-google-swe-book` SHOULD — Projects SHOULD follow the Google SWE Book ratio: 80% unit / 15% integration / 5% E2E.
- `e2e-tests` SHOULD — full system from user perspective. Expensive, brittle, SHOULD be used sparingly. Reserve for critical user journeys.
- `foundational-base-teams-pick-test-distribution-deliberately` SHOULD — The classic pyramid (many unit, fewer integration, fewest E2E) is a sensible default, not dogma. Some systems fit a …

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

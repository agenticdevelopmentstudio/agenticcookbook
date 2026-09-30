<!-- leaf: plan-testing/test-pyramid · source: guidelines/planning/testing/test-pyramid.md -->

**Rules** (cite as `plan-testing/test-pyramid#<slug>`):

- `projects-follow-google-swe-book` SHOULD — Projects SHOULD follow the Google SWE Book ratio: 80% unit / 15% integration / 5% E2E.
- `e2e-tests` SHOULD — full system from user perspective. Expensive, brittle, SHOULD be used sparingly. Reserve for critical user journeys.
- `default-dogma-teams-choose-test-distribution-per` SHOULD — The pyramid is a default, not dogma. Teams SHOULD choose the test distribution per system based on where risk actually …

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

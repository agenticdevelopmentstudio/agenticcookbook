
- **should-follow-the-80-15-5-ratio**: Projects SHOULD follow the Google SWE Book ratio: **80% unit / 15% integration / 5% E2E**.
- **should-use-real-dependencies-in-integration-tests**: Integration tests SHOULD use real databases, real file systems, real HTTP where practical.
- **should-use-e2e-tests-sparingly**: E2E tests SHOULD be used sparingly.
- **should-reserve-e2e-for-critical-journeys**: You SHOULD reserve E2E tests for critical user journeys.
- **should-default-to-a-unit-test**: If you're unsure what kind of test to write, you SHOULD write a unit test.
- **should-escalate-to-integration-when-unit-cannot-cover**: If the unit test can't cover the behavior (e.g., database queries, UI rendering), you SHOULD escalate to integration.
- **should-choose-the-distribution-per-system**: Teams SHOULD choose the test distribution per
  system based on where risk actually lives, not a fixed ratio. Teams SHOULD pick the
  test distribution deliberately, per system, based on where the real risk lives, rather than
  forcing a fixed ratio.
- **may-fit-the-testing-trophy**: Integration-heavy systems
  (thin logic over many collaborators — databases, queues, external services) MAY instead
  fit the "testing trophy" shape: a larger band of integration tests, with static analysis
  and type-checking as the broad base beneath them.
- **should-prefer-the-trophy-when-risk-is-in-interactions**: When most of the risk is in how
  components interact rather than in isolated logic, the trophy SHOULD be preferred over
  the pyramid.

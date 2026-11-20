
- `should-follow-the-80-15-5-ratio`: whether the suite's split is near 80% unit / 15% integration / 5% E2E, or a reason is given
- `should-use-real-dependencies-in-integration-tests`: whether integration tests use real databases, file systems and HTTP where practical
- `should-use-e2e-tests-sparingly`: whether E2E tests are used sparingly
- `should-reserve-e2e-for-critical-journeys`: whether every E2E test covers a critical user journey
- `should-default-to-a-unit-test`: whether unit tests were written where the kind of test was in doubt
- `should-escalate-to-integration-when-unit-cannot-cover`: whether behavior beyond a unit test's reach has an integration test
- `should-choose-the-distribution-per-system`: whether the distribution was chosen for this system's risk
- `may-fit-the-testing-trophy`: whether any trophy shape belongs to an integration-heavy system
- `should-prefer-the-trophy-when-risk-is-in-interactions`: whether a system whose risk is in interactions uses the trophy

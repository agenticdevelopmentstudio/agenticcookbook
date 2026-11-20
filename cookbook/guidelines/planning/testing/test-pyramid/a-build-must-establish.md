
- `should-follow-the-80-15-5-ratio`: the suite splits near 80% unit / 15% integration / 5% E2E, or the work says why not
- `should-use-real-dependencies-in-integration-tests`: integration tests run against real databases, file systems and HTTP where practical, or the work says why not
- `should-use-e2e-tests-sparingly`: E2E tests are few, or the work says why not
- `should-reserve-e2e-for-critical-journeys`: each E2E test names the critical user journey it covers, or the work says why not
- `should-default-to-a-unit-test`: behavior a unit test can cover is tested by a unit test, or the work says why not
- `should-escalate-to-integration-when-unit-cannot-cover`: behavior a unit test cannot cover has an integration test, or the work says why not
- `should-choose-the-distribution-per-system`: the chosen distribution names where this system's risk lives, or the work says why not
- `may-fit-the-testing-trophy`: any trophy shape is used for an integration-heavy system
- `should-prefer-the-trophy-when-risk-is-in-interactions`: a system whose risk is in interactions uses the trophy, or the work says why not

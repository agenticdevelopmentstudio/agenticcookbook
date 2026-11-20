
- `should-inform-unit-tests-with-property-based-testing`: property-based tests exist for the data transformations, or a note says why not
- `should-validate-test-quality-with-mutation-testing`: a mutation run's report is recorded, or a note says why not
- `must-write-tests-targeting-surviving-mutant-gaps`: the latest mutation report shows the earlier survivors killed by new tests
- `must-run-security-scan`: the semgrep and dependency-audit output is recorded for the change
- `should-verify-end-to-end`: an E2E run result (Playwright or the platform runner) is recorded, or a note says why not
- `must-execute-workflow-steps-in-order`: the workflow steps that ran were executed in order, and each skipped SHOULD step is stated with its reason
- `should-review-mutation-results-before-declaring-tests-complete`: mutation testing results were reviewed before the tests were declared complete, or the code says why not
- `should-cover-critical-user-journeys-in-e2e`: E2E verification covers the critical user journeys, or the code says why not

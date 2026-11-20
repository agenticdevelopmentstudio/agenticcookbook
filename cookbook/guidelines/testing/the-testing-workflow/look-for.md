
- `should-inform-unit-tests-with-property-based-testing`: data transformations tested only with hand-picked examples and no property-based tests
- `should-validate-test-quality-with-mutation-testing`: a test suite never put through a mutation run
- `must-write-tests-targeting-surviving-mutant-gaps`: surviving mutants with no added tests targeting them
- `must-run-security-scan`: no `semgrep scan` plus `bandit` / `pip-audit` / `npm audit` run in the workflow
- `should-verify-end-to-end`: a web UI with no Playwright tests, or a native app with no platform test-runner E2E tests
- `must-execute-all-workflow-steps-in-order`: a workflow with a step skipped or run out of order
- `should-review-mutation-results-before-declaring-tests-complete`: tests declared complete before the mutation testing results were reviewed
- `should-cover-critical-user-journeys-in-e2e`: E2E verification that leaves a critical user journey uncovered


- **should-inform-unit-tests-with-property-based-testing**: Unit tests SHOULD be written informed by property-based testing for data transformations.
- **should-validate-test-quality-with-mutation-testing**: After tests run, test quality SHOULD be validated with mutation testing (`mutmut run` / `npx stryker run` / `muter` / `dotnet stryker`).
- **must-write-tests-targeting-surviving-mutant-gaps**: To kill surviving mutants, additional tests MUST be written targeting gaps.
- **must-run-security-scan**: For the security scan, `semgrep scan` + `bandit` / `pip-audit` / `npm audit` MUST be run.
- **should-verify-end-to-end**: E2E verification SHOULD use Playwright for web UIs and platform test runners for native.
- **must-execute-workflow-steps-in-order**: The workflow steps that run MUST be executed in order, and a SHOULD step that is skipped (mutation testing, E2E verification) MUST be stated with its reason.
- **should-review-mutation-results-before-declaring-tests-complete**: Mutation testing results SHOULD be reviewed before tests are declared complete.
- **should-cover-critical-user-journeys-in-e2e**: E2E verification SHOULD cover critical user journeys.

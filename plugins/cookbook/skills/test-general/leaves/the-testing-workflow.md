<!-- leaf: test-general/the-testing-workflow · source: guidelines/testing/the-testing-workflow.md -->

**Rules** (cite as `test-general/the-testing-workflow#<slug>`):

- `kill-surviving-mutants` MUST — additional tests MUST be written targeting gaps
- `security-scan` MUST — semgrep scan + bandit / pip-audit / npm audit MUST be run

# The Testing Workflow

The recommended Claude Code testing workflow, combining all tools:

1. **Write implementation code**
2. **Write unit tests** — informed by property-based testing for data transformations
3. **Run tests** — `pytest` / `swift test` / `npm test` / `dotnet test`
4. **Validate test quality** — `mutmut run` / `npx stryker run` / `muter` / `dotnet stryker`
5. **Kill surviving mutants** — additional tests MUST be written targeting gaps
6. **Security scan** — `semgrep scan` + `bandit` / `pip-audit` / `npm audit` MUST be run
7. **E2E verification** — Playwright for web UIs, platform test runners for native

This creates a closed loop: AI generates tests, deterministic tools validate those tests
actually catch bugs, AI writes more tests to close gaps.

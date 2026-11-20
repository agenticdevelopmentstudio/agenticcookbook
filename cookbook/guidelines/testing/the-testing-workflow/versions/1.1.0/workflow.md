
The recommended Claude Code testing workflow, combining all tools:

1. **Write implementation code**
2. **Write unit tests** — informed by property-based testing for data transformations
3. **Run tests** — `pytest` / `swift test` / `npm test` / `dotnet test`
4. **Validate test quality** — `mutmut run` / `npx stryker run` / `muter` / `dotnet stryker`
5. **Kill surviving mutants**
6. **Security scan** — `semgrep scan` + `bandit` / `pip-audit` / `npm audit`
7. **E2E verification** — Playwright for web UIs, platform test runners for native

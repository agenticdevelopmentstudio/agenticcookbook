<!-- leaf: test-general/mutation-testing · source: guidelines/testing/mutation-testing.md -->

**Rules** (cite as `test-general/mutation-testing#<slug>`):

- `mutants-surviving-mutants-addressed` MUST — Write additional tests to kill surviving mutants — all surviving mutants MUST be addressed
- `mutation-testing-must-be-run-before-claiming-tests-are-complete` MUST — 

# Mutation Testing

Mutation testing validates that your tests actually catch bugs — not just achieve coverage.

**How it works:** The tool mutates your source code (e.g., changes `<` to `<=`, `True` to
`False`, deletes a line) and re-runs your tests. If tests still pass, the mutant "survived"
— meaning your tests have a blind spot.

**The closed loop:**
1. Write tests
2. Run mutation testing
3. Examine surviving mutants
4. Write additional tests to kill surviving mutants — all surviving mutants MUST be addressed
5. Repeat until mutation score is acceptable

**Mutation testing MUST be run before claiming "tests are complete."**

**Platform tools:**

| Platform | Tool | Install | Run |
|----------|------|---------|-----|
| Python | [mutmut](https://github.com/boxed/mutmut) | `pip install mutmut` | `mutmut run` |
| TypeScript/JS | [Stryker](https://stryker-mutator.io/) | `npm i -g stryker-cli` | `npx stryker run` |
| .NET | [Stryker.NET](https://stryker-mutator.io/) | `dotnet tool install -g dotnet-stryker` | `dotnet stryker` |
| Swift | [Muter](https://github.com/muter-mutation-testing/muter) | `brew install muter-mutation-testing/formulae/muter` | `muter` |
| Kotlin/JVM | [Pitest](https://pitest.org/) | Gradle/Maven plugin | `./gradlew pitest` |

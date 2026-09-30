<!-- leaf: test-general/linting · source: guidelines/testing/linting.md -->

**Rules** (cite as `test-general/linting#<slug>`):

- `linting-run-part-automated-verification` MUST — Linting MUST run as part of the automated verification process:
- `in-ci` MUST — linting failures MUST block the build alongside test failures
- `after-code-generation` MUST — AI-generated code MUST pass linting before being accepted

# Linting as automated verification

Linting is part of your test suite — it catches categories of bugs that unit tests miss (unused imports, unreachable code, security anti-patterns, style violations that affect readability).

## When to run

Linting MUST run as part of the automated verification process:
- **During development** — as part of the build or pre-commit hook
- **In CI** — linting failures MUST block the build alongside test failures
- **After code generation** — AI-generated code MUST pass linting before being accepted

## What linting verifies that tests don't

- Unused variables, imports, and dead code
- Security anti-patterns (eval, innerHTML, SQL string concatenation)
- Formatting inconsistencies that harm readability
- Language-specific pitfalls (force-unwraps in Swift, non-null assertions in TypeScript)

## Platform linters

| Platform | Linter | Formatter |
|----------|--------|-----------|
| Swift | SwiftLint | swift-format |
| Kotlin | ktlint | ktlint |
| TypeScript | ESLint | Prettier |
| C# / .NET | Roslyn Analyzers + .editorconfig | dotnet format |

See the implementing copy of this guideline for platform-specific setup details.

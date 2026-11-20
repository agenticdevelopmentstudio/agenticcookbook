
# Linting before the first PR

All projects MUST have linting configured and passing before the first pull request. Linting config SHOULD be set up early in the project, but during rapid prototyping, committing without lint-gating every commit is acceptable. Before any PR is opened, lint MUST be clean.

| Platform | Linter | Formatter |
|----------|--------|-----------|
| Swift | SwiftLint | swift-format |
| Kotlin | ktlint | ktlint |
| TypeScript | ESLint | Prettier |
| C# / .NET | Roslyn Analyzers + .editorconfig | dotnet format |

Linter config MUST be committed. Linting MUST run as part of the build or pre-commit process. Formatting MUST be auto-fixable.


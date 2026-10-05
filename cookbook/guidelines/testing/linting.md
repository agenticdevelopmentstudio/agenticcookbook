---
id: 34f13883-8905-4b5c-9299-82602687e98d
title: "Linting from day one"
domain: agenticdevelopercookbook://guidelines/testing/linting
type: guideline
version: 1.1.2
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Run linting as part of your automated test and verification suite — it catches bugs that unit tests miss."
platforms:
  - csharp
  - kotlin
  - swift
  - typescript
  - web
tags:
  - code-quality
  - linting
depends-on: []
related: []
references:
  - https://eslint.org/
  - https://github.com/dotnet/roslynator
  - https://github.com/meziantou/Meziantou.Analyzer
  - https://github.com/realm/SwiftLint
  - https://github.com/swiftlang/swift-format
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/
  - https://pinterest.github.io/ktlint/
  - https://prettier.io/
  - https://stylelint.io/
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
triggers:
  - pre-commit
  - new-module
---

# Linting from day one

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.2 | 2026-10-04 | Mike Fullerton | Add the statement under the title (or align the title line) that the guideline format requires |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for testing use case — reframe as automated verification tool |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

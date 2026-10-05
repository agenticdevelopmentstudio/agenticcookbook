---
id: e79fe94e-cc8a-4fb8-985c-1b9bfc4c5c12
title: .NET & Windows Development Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/windows/dotnet-tooling
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: .NET & Windows Development Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# .NET & Windows Development Tools

**Date:** 2026-03-29
**Context:** .NET/C# development tools that integrate with Claude Code for the plan/implement/verify loop.

This catalog covers best-in-class CLI tools for .NET and Windows development, organized by category. Each entry notes the tool's loop phase (plan, implement, verify), install command, and integration method with Claude Code.

**Integration methods:**
- **CLI shell-out** -- Claude Code runs the tool via Bash/PowerShell (most common)
- **MCP server** -- tool exposes a Model Context Protocol server for direct integration
- **Hook** -- Claude Code pre/post-tool hook triggers the tool automatically
- **Plugin** -- Claude Code plugin bundles MCP + hooks + skills

---

## Linters & Formatters (implement/verify)

Tools for enforcing code style, formatting, and consistency. All integrate via CLI shell-out. The modern .NET approach layers EditorConfig (style rules) + `dotnet format` (enforcement) + optional third-party analyzers (extended rules) + an opinionated formatter (whitespace).

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [dotnet format](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format) | Built-in SDK formatter and linter (since .NET 6). Enforces `.editorconfig` rules for whitespace, code style, and analyzer diagnostics. Three subcommands: `whitespace`, `style`, `analyzers`. | Included with .NET SDK 6+ | Core tool for Claude Code. Run `dotnet format --verify-no-changes` in verify phase to check; `dotnet format` in implement phase to auto-fix. Reads `.editorconfig` from the project tree. |
| [EditorConfig](https://editorconfig.org/) | Configuration file (`.editorconfig`) that defines code style rules consumed by `dotnet format`, Roslyn analyzers, and IDEs. Supports .NET-specific rules like `dotnet_style_*` and `csharp_style_*`. | Drop a `.editorconfig` file in the repo root | Not a tool itself but the configuration backbone. Claude Code can read and edit `.editorconfig` to adjust rules. Microsoft publishes a [comprehensive reference](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/code-style-rule-options). |
| [StyleCop Analyzers](https://github.com/DotNetAnalyzers/StyleCopAnalyzers) | Roslyn-based analyzers enforcing StyleCop's layout, ordering, spacing, readability, and documentation rules. ~200 rules with SA-prefix diagnostic IDs. | `dotnet add package StyleCop.Analyzers` | Mature but less actively maintained than Roslynator. Best for teams migrating from legacy StyleCop. Claude Code runs `dotnet format analyzers --severity info` to surface violations. |
| [Roslynator](https://github.com/dotnet/roslynator) | 500+ analyzers, refactorings, and code fixes for C#, powered by Roslyn. Actively maintained under the `dotnet` GitHub org. Analyzers package contains 200+ diagnostic rules; refactorings package adds 200+ more. | `dotnet add package Roslynator.Analyzers` | The recommended general-purpose analyzer suite. Claude Code surfaces diagnostics via `dotnet build` warnings or `dotnet format analyzers`. Configure severity in `.editorconfig` with `dotnet_diagnostic.RCSxxxx.severity`. |
| [Meziantou.Analyzer](https://github.com/meziantou/Meziantou.Analyzer) | Roslyn analyzer enforcing best practices for performance, security, usage, and design in C#. Actively maintained with frequent releases. | `dotnet add package Meziantou.Analyzer` | Complements Roslynator with unique rules (e.g., MA0004 for `Task.ConfigureAwait`, MA0006 for string comparison). Set `MeziantouAnalysisMode` in `Directory.Build.props` to control default severity. |
| [CSharpier](https://csharpier.com/) | Opinionated code formatter for C# (inspired by Prettier). Parses and re-prints code using its own rules, eliminating style debates. Minimal configuration by design. v1.2.6 is current. | `dotnet tool install -g csharpier` | Ideal as a hook or format-on-save. Claude Code runs `dotnet csharpier .` to format all files. Pair with `dotnet format` for the full pipeline: CSharpier handles whitespace/layout, `dotnet format` handles style diagnostics. |

---

## Testing Frameworks (verify)

.NET testing tools for unit, integration, snapshot, and mutation testing. All integrate via `dotnet test` CLI shell-out.

### Test Runners

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [xUnit](https://xunit.net/) | The most widely adopted .NET test framework. Default in Visual Studio templates, 469M+ NuGet downloads, used by 65%+ of C# open-source projects. Supports parallel execution, theory/data-driven tests, and extensible assertions. | `dotnet add package xunit` + `dotnet add package xunit.runner.visualstudio` | Recommended default. Claude Code runs `dotnet test` to execute. xUnit's `[Fact]` and `[Theory]` attributes are well-known in training data. |
| [NUnit](https://nunit.org/) | Mature framework with rich attribute-driven configuration (`[TestCase]`, `[SetUp]`, `[TearDown]`, custom constraints). Best for legacy codebases and teams needing parameterized test metadata. | `dotnet add package NUnit` + `dotnet add package NUnit3TestAdapter` | Strong for data-driven scenarios. Claude Code runs `dotnet test` identically to xUnit. |
| [MSTest](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-mstest) | Microsoft's built-in test framework, included with Visual Studio. MSTest v3/v4 are modern and competitive. Simplest setup for new developers. | `dotnet add package MSTest.TestFramework` + `dotnet add package MSTest.TestAdapter` | Good default for teams standardizing on Microsoft tooling. Same `dotnet test` integration. |

### Assertion Libraries

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [FluentAssertions](https://fluentassertions.com/) | Fluent assertion syntax for readable test expectations. Supports xUnit, NUnit, MSTest, MSpec, and TUnit. Rich failure messages with expected/actual diffs. | `dotnet add package FluentAssertions` | Most popular assertion library. `result.Should().Be(42)` reads naturally. Claude Code generates fluent assertions by default when this package is present. |
| [Shouldly](https://docs.shouldly.org/) | Terse assertion library focused on great error messages. Extension-method syntax: `result.ShouldBe(42)`. v4.3.0 targets .NET 8+ and .NET Standard 2.0. | `dotnet add package Shouldly` | Lighter alternative to FluentAssertions. Smaller API surface, fewer dependencies. |

### Mocking

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [NSubstitute](https://nsubstitute.github.io/) | Friendly mocking library with clean syntax. `Substitute.For<IService>()` creates mocks with minimal ceremony. No `Setup`/`Verify` boilerplate. | `dotnet add package NSubstitute` | Recommended for new projects. Simplest API of the major mocking libraries. Claude Code prefers NSubstitute's concise syntax. |
| [Moq](https://github.com/devlooped/moq) | Strongly-typed mocking with `Setup`/`Verify` pattern. More control over mock behavior at the cost of verbosity. Widely used in enterprise codebases. | `dotnet add package Moq` | Mature and battle-tested. Note: Moq 4.20 (2023) had a telemetry controversy; many teams migrated to NSubstitute. Still widely used. |
| [FakeItEasy](https://fakeiteasy.github.io/) | Simple mocking library with a focus on ease of use. `A.Fake<IService>()` creates fakes. Syntax falls between NSubstitute's brevity and Moq's explicitness. | `dotnet add package FakeItEasy` | Third option when neither NSubstitute nor Moq fits the team's preference. |

### Test Data Generation

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Bogus](https://github.com/bchavez/Bogus) | Fake data generator for .NET. Generates realistic names, emails, addresses, dates, and domain-specific data using a fluent API. Inspired by faker.js. | `dotnet add package Bogus` | Claude Code uses Bogus to generate seed data and test fixtures. `new Faker<User>().RuleFor(u => u.Name, f => f.Name.FullName())`. |
| [AutoFixture](https://autofixture.github.io/) | Automatic test object creation. Generates anonymous instances of any class, filling properties with random but valid data. Integrates with xUnit, NUnit, NSubstitute, Moq. | `dotnet add package AutoFixture` + `dotnet add package AutoFixture.AutoNSubstitute` | Eliminates manual test object setup. `fixture.Create<User>()` generates a fully populated instance. Combine with NSubstitute for auto-mocking. |

### Snapshot Testing

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Verify](https://github.com/VerifyTests/Verify) | Snapshot testing for .NET. Serializes test output to a `.verified.txt` file and diffs against it on subsequent runs. Supports xUnit, NUnit, MSTest, and Expecto. | `dotnet add package Verify.Xunit` (or `Verify.NUnit` / `Verify.MSTest`) | Run `dotnet test` as usual. On first run, accept snapshots with the Verify CLI tool or IDE plugin. Claude Code can update `.verified.txt` files when behavior intentionally changes. |

### Mutation Testing

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Stryker.NET](https://stryker-mutator.io/docs/stryker-net/introduction/) | Mutation testing for .NET. Automatically mutates source code (flips conditionals, removes statements, changes operators) and verifies tests catch the mutations. Generates a mutation score report. | `dotnet tool install -g dotnet-stryker` | Run from the test project directory: `dotnet stryker`. Configure via `stryker-config.json`. Claude Code can analyze the HTML report to identify weak test coverage. Now referenced in [Microsoft's official docs](https://learn.microsoft.com/en-us/dotnet/core/testing/mutation-testing). |

---

## Static Analysis (verify)

Tools that analyze code without executing it, catching bugs, security issues, and design problems. Most integrate as Roslyn analyzer NuGet packages, surfaced through `dotnet build` warnings.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [.NET Analyzers (CA rules)](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview) | Built-in Roslyn analyzers included with the .NET SDK. CA-prefix rules cover security, performance, design, globalization, and reliability. IDE-prefix rules cover code style. | Included with .NET SDK; enable with `<EnableNETAnalyzers>true</EnableNETAnalyzers>` | Foundation layer -- always enabled. Claude Code reads CA warnings from `dotnet build` output. Configure severity per-rule in `.editorconfig`: `dotnet_diagnostic.CA1062.severity = warning`. |
| [SonarAnalyzer.CSharp](https://github.com/SonarSource/sonar-dotnet) | 380+ C# rules and 130+ VB.NET rules from SonarSource. Covers bugs, vulnerabilities, code smells, and security hotspots. Works standalone (NuGet) or with SonarQube/SonarCloud. | `dotnet add package SonarAnalyzer.CSharp` | Strong security and reliability rules that go beyond built-in CA rules. Claude Code surfaces violations via `dotnet build`. For full pipeline integration, pair with `dotnet-sonarscanner`. |
| [Semgrep](https://semgrep.dev/docs/languages/csharp) | Lightweight static analysis supporting 30+ languages including C# (GA). Pattern-based rules that look like source code. Semgrep Supply Chain scans NuGet dependencies for reachable vulnerabilities. | `pip install semgrep` or `brew install semgrep` | CLI shell-out: `semgrep scan --config auto`. Framework-specific Pro rules require `semgrep login && semgrep ci`. Fall 2025 release added 3x performance (multicore) and native Windows support. |
| [SecurityCodeScan](https://security-code-scan.github.io/) | Vulnerability pattern detector for C# and VB.NET. Detects SQL injection, XSS, CSRF, XXE, and other OWASP Top 10 issues. | `dotnet add package SecurityCodeScan.VS2019` | Lighter alternative to SonarAnalyzer for security-only scanning. Note: less actively maintained than SonarAnalyzer as of 2025; SonarAnalyzer.CSharp is now the stronger recommendation for security rules. |
| [NDepend](https://www.ndepend.com/) | Enterprise static analysis with deep interprocedural flow analysis, cross-project dependency mapping, architectural rule enforcement, and technical debt tracking. 150+ default code rules. | Commercial license; CLI via `NDepend.Console.exe` | Goes far beyond Roslyn analyzers for architectural governance. CLI shell-out for CI. Not free, but the only tool offering dependency structure matrix, code metrics trends, and custom CQLinq rules. |

---

## Build Tooling (implement/verify)

Core build, publish, and project configuration tools. The `dotnet` CLI is the primary interface; MSBuild handles the build engine underneath.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [dotnet CLI](https://learn.microsoft.com/en-us/dotnet/core/tools/) | Unified CLI for building, testing, publishing, packaging, and managing .NET projects. Core commands: `build`, `test`, `run`, `publish`, `pack`, `tool`, `new`. | Included with .NET SDK | The single most important tool for Claude Code .NET integration. Every phase uses it: `dotnet new` (plan/implement), `dotnet build` (implement), `dotnet test` (verify), `dotnet publish` (implement). |
| [MSBuild](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild) | The build engine behind `dotnet build`. Direct `msbuild` commands give finer control: custom targets, property evaluation (`-getProperty`), binary logging (`-bl`). | Included with .NET SDK / Visual Studio | Claude Code uses `dotnet msbuild -getProperty:TargetFramework` to query project properties. Binary logs (`msbuild -bl`) can be analyzed with [MSBuild Structured Log Viewer](https://msbuildlog.com/). |
| [Directory.Build.props](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-your-build) | MSBuild file placed at the repo root that applies common properties to all projects in the solution. Centralizes `<LangVersion>`, `<Nullable>`, `<TreatWarningsAsErrors>`, analyzer packages, etc. | Create `Directory.Build.props` at repo root | Essential for multi-project solutions. Claude Code reads this file to understand repo-wide settings and edits it to apply changes across all projects at once. |
| [Directory.Build.targets](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-your-build) | Like `Directory.Build.props` but evaluated after individual project files. Used for custom build targets, post-build steps, and conditional logic that depends on per-project properties. | Create `Directory.Build.targets` at repo root | Less common than `.props` but important for advanced scenarios (e.g., running analyzers only on src projects, not test projects). |
| [Central Package Management](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management) | Centralizes NuGet package versions in a single `Directory.Packages.props` file. Projects use `<PackageReference>` without `Version`; versions are resolved from the central file. | Create `Directory.Packages.props` with `<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>` | Prevents version drift across projects. Claude Code edits one file to upgrade a dependency everywhere. Transitive pinning (`<CentralPackageTransitivePinningEnabled>true`) also secures transitive dependencies. |
| [global.json](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json) | Pins the .NET SDK version for the repo. Ensures consistent builds across developer machines and CI. | Create `global.json` at repo root | Claude Code reads this to know which SDK version to target. `dotnet new globaljson --sdk-version 9.0.100` creates it. |

---

## Code Generation (implement)

Tools that generate C# code at compile time or design time, reducing boilerplate.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Roslyn Source Generators](https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/source-generators-overview) | Compile-time code generation with full access to the Roslyn semantic model. Runs as part of every build, zero runtime overhead, full IDE support. The `IIncrementalGenerator` API (Roslyn 4.0+/.NET 6+) is the modern standard. | Authored as a class library targeting `netstandard2.0` with `Microsoft.CodeAnalysis.CSharp` dependency | Claude Code can author source generators for serialization, DI registration, mapping, and API clients. Generated code appears in `obj/` and is visible to IntelliSense. Prefer incremental generators over the legacy `ISourceGenerator` API. |
| [T4 Templates](https://learn.microsoft.com/en-us/visualstudio/modeling/code-generation-and-t4-text-templates) | Text template engine for generating any text output (C#, SQL, config, HTML). Available since .NET 3.5. Runs outside the build pipeline by default, though [T4.SourceGenerator](https://github.com/CptWesley/T4.SourceGenerator) bridges to Roslyn. | Built into Visual Studio; CLI via `dotnet-t4` tool | Best for non-code output (SQL scripts, HTML, config files). For C# code generation, prefer source generators. EF Core 7+ restored T4 support for database-first scaffolding customization. |
| [dotnet new (templates)](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-new) | Project and item scaffolding. Built-in templates for webapi, console, classlib, blazor, etc. Custom templates via `template.json`. | Included with .NET SDK | Claude Code runs `dotnet new webapi -n MyService` to scaffold projects. `dotnet new list` shows available templates. Custom templates let teams standardize project structure. |
| [EF Core Scaffolding](https://learn.microsoft.com/en-us/ef/core/managing-schemas/scaffolding/) | Reverse-engineers a database into C# entity classes and a DbContext. Supports T4 template customization for output format. | `dotnet tool install -g dotnet-ef` | CLI shell-out: `dotnet ef dbcontext scaffold "connection-string" Microsoft.EntityFrameworkCore.SqlServer`. Claude Code can customize the generated output via T4 templates. |

---

## Package Management (implement)

NuGet package installation, version management, and security auditing. All via CLI shell-out.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [dotnet add package](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-add-package) | Adds a NuGet package reference to a project file. Resolves the latest stable version by default, or a specified version. | Included with .NET SDK | Primary package install command. Claude Code runs `dotnet add package Newtonsoft.Json` to add dependencies. With CPM, omit the version -- it comes from `Directory.Packages.props`. |
| [dotnet list package](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-list-package) | Lists all package references for a project or solution. Flags: `--vulnerable`, `--deprecated`, `--outdated`, `--include-transitive`. | Included with .NET SDK | Key verify-phase tool. `dotnet list package --vulnerable --include-transitive` surfaces known CVEs. `dotnet list package --outdated` shows available upgrades. |
| [NuGet Audit](https://devblogs.microsoft.com/dotnet/nugetaudit-2-0-elevating-security-and-trust-in-package-management/) | Automatic vulnerability scanning during `dotnet restore`. NuGet Audit 2.0 scans direct and transitive dependencies against the GitHub Advisory Database. In .NET 10+, audit mode defaults to "all" (direct + transitive). | Enabled by default in .NET 8+; configure via `<NuGetAudit>true</NuGetAudit>` | Passive security -- runs on every restore/build without explicit invocation. Claude Code sees audit warnings in `dotnet build` output. Set `<NuGetAuditLevel>low</NuGetAuditLevel>` for strictest scanning. |
| [NuGet CLI (nuget.exe)](https://learn.microsoft.com/en-us/nuget/reference/nuget-exe-cli-reference) | Standalone NuGet command-line tool for restore, pack, push, and config management. Required for some .NET Framework scenarios. | `winget install Microsoft.NuGet` or download from [nuget.org](https://www.nuget.org/downloads) | Mostly superseded by `dotnet` CLI for .NET Core/5+ projects. Still needed for .NET Framework projects or advanced NuGet operations (e.g., `nuget sources`, `nuget sign`). |

---

## Documentation (implement)

Tools for generating API documentation from C# source code and XML comments.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [XML Documentation Comments](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/) | Triple-slash (`///`) comments with XML tags (`<summary>`, `<param>`, `<returns>`, `<exception>`, `<example>`). Compiler generates `.xml` files consumed by IntelliSense and doc generators. | Built into C#; enable with `<GenerateDocumentationFile>true</GenerateDocumentationFile>` | Claude Code generates XML doc comments for public APIs. Set `<NoWarn>` to suppress CS1591 (missing XML comment) for internal code, or enforce it for public libraries. |
| [DocFX](https://dotnet.github.io/docfx/) | Microsoft's static site generator for .NET API documentation. Consumes XML doc comments and Markdown to produce a searchable HTML site. Supports C#, VB.NET, and F#. The successor to Sandcastle. | `dotnet tool install -g docfx` | CLI shell-out: `docfx init`, `docfx build`, `docfx serve`. Claude Code can generate and update Markdown articles alongside auto-generated API docs. |
| [Sandcastle Help File Builder](https://github.com/EWSoftware/SHFB) | Legacy documentation generator producing CHM, MSHV, and website output from XML comments. Command-line based, no GUI. | Download from GitHub releases | Effectively superseded by DocFX for new projects. Use only if you need CHM/Help Viewer output or are maintaining an existing Sandcastle pipeline. |

---

## Dependency Security (verify)

Tools for finding vulnerable, deprecated, or abandoned packages in .NET projects.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [dotnet list package --vulnerable](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-list-package) | Lists packages with known security vulnerabilities from the GitHub Advisory Database. Add `--include-transitive` to scan the full dependency graph. | Included with .NET SDK | First-line defense. Claude Code runs `dotnet list package --vulnerable --include-transitive` in the verify phase. Zero dependencies beyond the SDK. |
| [NuGet Audit](https://devblogs.microsoft.com/dotnet/nugetaudit-2-0-elevating-security-and-trust-in-package-management/) | Automatic vulnerability scanning on every `dotnet restore`. NuGet Audit 2.0 scans both direct and transitive dependencies. In .NET 10+, defaults to scanning all dependencies. | Enabled by default in .NET 8+ | Passive -- no explicit invocation needed. Warnings appear in build output. Configure `<NuGetAuditMode>all</NuGetAuditMode>` and `<NuGetAuditLevel>low</NuGetAuditLevel>` in `Directory.Build.props` for strictest scanning. |
| [dotnet list package --deprecated](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-list-package) | Lists packages marked as deprecated by their authors, including suggested replacements. | Included with .NET SDK | Run periodically to catch abandoned dependencies before they become security risks. Claude Code can flag deprecated packages and suggest alternatives. |
| [Snyk .NET](https://docs.snyk.io/supported-languages-package-managers-and-frameworks/.net/guidance-for-snyk-for-.net) | Commercial SCA platform with .NET/NuGet support. Scans for vulnerabilities, provides remediation advice, and monitors continuously. Integrates with CI/CD via GitHub Actions (`snyk/actions/dotnet`). | `npm install -g snyk` then `snyk auth` | Broader vulnerability database than NuGet Audit alone. Free tier covers open-source projects. CLI shell-out: `snyk test --all-projects`. |
| [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/) | Open-source SCA tool scanning project dependencies against the NVD (National Vulnerability Database). Supports .NET via CLI or plugins. | Download CLI from [GitHub releases](https://github.com/jeremylong/DependencyCheck/releases) | Free and open-source alternative to Snyk. Caveat: struggles with .NET property substitution (e.g., `Directory.Build.props` references) causing false positives. Best paired with `dotnet list package --vulnerable` for .NET-specific accuracy. |

---

## Performance Profiling (verify)

Tools for benchmarking, tracing, and diagnosing .NET application performance. All integrate via CLI shell-out.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [BenchmarkDotNet](https://benchmarkdotnet.org/) | The standard .NET microbenchmarking library. Automates warmup, iteration, and statistical analysis. Produces markdown/HTML reports with execution time, memory allocation, and GC metrics. Used by Microsoft and .NET OSS maintainers. | `dotnet add package BenchmarkDotNet` | Claude Code generates `[Benchmark]`-attributed methods and runs `dotnet run -c Release` from the benchmark project. Results are deterministic and comparable across runs. |
| [dotnet-counters](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-counters) | Live performance monitoring for running .NET processes. Displays EventCounter and Meter API values (CPU, GC, threadpool, exceptions, custom counters) in real time. | `dotnet tool install -g dotnet-counters` | First-level performance triage. `dotnet-counters monitor --process-id <pid>` shows live metrics. `dotnet-counters collect` exports to CSV/JSON for analysis. |
| [dotnet-trace](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace) | Collects detailed runtime traces from a running .NET process without a native debugger. Exports to `.nettrace` format (convertible to `.speedscope.json` or Chromium trace). | `dotnet tool install -g dotnet-trace` | Cross-platform (works on Linux, macOS, Windows). `dotnet-trace collect --process-id <pid>` captures CPU, GC, and allocation events. Open traces in [speedscope](https://www.speedscope.app/) or PerfView. |
| [dotnet-dump](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-dump) | Collects and analyzes process dumps without a native debugger. Supports SOS debugging commands (`dumpheap`, `dumpobj`, `gcroot`) for memory leak investigation. | `dotnet tool install -g dotnet-dump` | `dotnet-dump collect --process-id <pid>` captures a dump. `dotnet-dump analyze <dump-file>` opens an interactive session. Claude Code can run SOS commands to diagnose memory issues. |
| [dotnet-gcdump](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-gcdump) | Collects GC (garbage collector) dumps showing live object graphs. Lighter than a full process dump -- captures only managed heap information. | `dotnet tool install -g dotnet-gcdump` | `dotnet-gcdump collect --process-id <pid>` exports a `.gcdump` file. Useful for identifying memory leaks without the overhead of a full dump. |
| [PerfView](https://github.com/Microsoft/perfview) | Microsoft's free advanced performance analysis tool for Windows. Analyzes ETW traces, GC behavior, JIT compilation, CPU sampling, and memory allocation. Steep learning curve but unmatched depth. | Download from [GitHub releases](https://github.com/microsoft/perfview/releases) | Windows-only. BenchmarkDotNet's `EtwProfiler` can generate PerfView-compatible traces automatically. Claude Code can trigger collection but analysis is best done interactively in the PerfView GUI. |
| [dotnet-monitor](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-monitor) | Sidecar diagnostic tool that exposes REST APIs for collecting traces, dumps, counters, and logs from running .NET apps. Designed for containerized/production environments. | `dotnet tool install -g dotnet-monitor` | Exposes HTTP endpoints for diagnostics without direct process access. Ideal for Kubernetes/container scenarios where SSH is unavailable. Claude Code can `curl` the endpoints to trigger collections. |

---

## Sources

- [Microsoft .NET CLI Documentation](https://learn.microsoft.com/en-us/dotnet/core/tools/)
- [Microsoft Code Analysis Overview](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview)
- [Microsoft Central Package Management](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management)
- [Microsoft .NET Diagnostics Tools](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/)
- [NuGet Audit 2.0 Blog Post](https://devblogs.microsoft.com/dotnet/nugetaudit-2-0-elevating-security-and-trust-in-package-management/)
- [Roslynator GitHub (dotnet org)](https://github.com/dotnet/roslynator)
- [Meziantou.Analyzer GitHub](https://github.com/meziantou/Meziantou.Analyzer)
- [CSharpier Official Site](https://csharpier.com/)
- [StyleCop Analyzers GitHub](https://github.com/DotNetAnalyzers/StyleCopAnalyzers)
- [SonarSource sonar-dotnet GitHub](https://github.com/SonarSource/sonar-dotnet)
- [Semgrep C# Language Support](https://semgrep.dev/docs/languages/csharp)
- [Stryker.NET Documentation](https://stryker-mutator.io/docs/stryker-net/introduction/)
- [Verify Snapshot Testing GitHub](https://github.com/VerifyTests/Verify)
- [BenchmarkDotNet GitHub](https://github.com/dotnet/BenchmarkDotNet)
- [DocFX Official Site](https://dotnet.github.io/docfx/)
- [Snyk .NET Guidance](https://docs.snyk.io/supported-languages-package-managers-and-frameworks/.net/guidance-for-snyk-for-.net)
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [PerfView GitHub](https://github.com/Microsoft/perfview)
- [xUnit.net](https://xunit.net/)
- [FluentAssertions](https://fluentassertions.com/)
- [NSubstitute](https://nsubstitute.github.io/)
- [Bogus GitHub](https://github.com/bchavez/Bogus)
- [AutoFixture](https://autofixture.github.io/)
- [C# Source Generators Guide](https://www.devleader.ca/2026/03/16/c-source-generators-a-complete-guide-to-compiletime-code-generation)
- [How to Start a New .NET Project in 2026](https://antondevtips.com/blog/how-to-start-a-new-dotnet-project-in-2026)

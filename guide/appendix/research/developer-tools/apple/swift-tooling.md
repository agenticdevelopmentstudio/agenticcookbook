---
id: d465658a-3e5f-4b48-abe2-673ff3d0dba5
title: Swift & SwiftUI Development Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/apple/swift-tooling
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Swift & SwiftUI Development Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Swift & SwiftUI Development Tools

**Date:** 2026-03-29
**Context:** Tools for Swift/SwiftUI development across all Apple platforms, integrated with Claude Code.

---

## Linters & Formatters (implement/verify)

### SwiftLint

- **Link:** [github.com/realm/SwiftLint](https://github.com/realm/SwiftLint)
- **Description:** The de facto standard linter for Swift. Enforces style and conventions based on community-accepted rules. Supports over 200 configurable rules (lint rules and opt-in analyzer rules). Configuration via `.swiftlint.yml`. Analyzer mode (`swiftlint analyze`) uses the full type-checked AST for deeper static analysis (slower, opt-in). Supports baselines to diff violations against a known state. Swift 6 compatible.
- **Loop phase:** implement (real-time feedback), verify (CI gate)
- **Install:**
  ```bash
  brew install swiftlint                         # Homebrew
  mint install realm/SwiftLint                   # Mint
  # Or add SwiftLintPlugins as SPM dependency
  ```
- **Claude Code integration:** Shell out to `swiftlint lint --path <file>` or `swiftlint lint --reporter json` for structured output. Use `swiftlint analyze --compiler-log-path <log>` for deeper analysis. Parse JSON reporter output for actionable diagnostics.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS (runs on macOS and Linux)

### SwiftFormat (Nick Lockwood)

- **Link:** [github.com/nicklockwood/SwiftFormat](https://github.com/nicklockwood/SwiftFormat)
- **Description:** Opinionated code formatter that adjusts whitespace, removes redundant syntax (parentheses, `self`, etc.), and enforces consistent style. Over 70 formatting rules. Highly configurable via `.swiftformat` config file. Can infer project style with `--infer-options`. Actively maintained with version 0.55+.
- **Loop phase:** implement (format-on-save), verify (CI check)
- **Install:**
  ```bash
  brew install swiftformat
  mint install nicklockwood/SwiftFormat
  ```
- **Claude Code integration:** Shell out to `swiftformat <path> --dryrun --verbose` to preview changes, or `swiftformat <path>` to apply. Use `swiftformat stdin` for piping. Supports `--lint` mode that reports without modifying (exit code 1 on violations).
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS (runs on macOS, Linux, Windows)

### swift-format (Apple Official)

- **Link:** [github.com/swiftlang/swift-format](https://github.com/swiftlang/swift-format)
- **Description:** Apple's official formatting technology, built on SwiftSyntax. Included in the Swift 6+ toolchain (invoked as `swift format` with a space). Provides both formatting and linting. No official Swift style guide yet -- the style applied is one possibility. Configuration via `.swift-format` JSON file. Used by SourceKit-LSP.
- **Loop phase:** implement (format-on-save), verify (CI check)
- **Install:**
  ```bash
  # Included with Swift 6+ toolchain / Xcode 16+
  swift format --version
  # Or as SPM dependency:
  .package(url: "https://github.com/swiftlang/swift-format", from: "600.0.0")
  ```
- **Claude Code integration:** Shell out to `swift format <file>` to format, `swift format lint <file>` to lint. JSON output not natively supported; parse stderr for diagnostics. Best for projects that want to stay purely within Apple's toolchain.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS (runs on macOS and Linux)

### Periphery

- **Link:** [github.com/peripheryapp/periphery](https://github.com/peripheryapp/periphery)
- **Description:** Static analysis tool that detects unused Swift code -- classes, structs, protocols, functions, properties, enum cases, function parameters, protocol conformances, and redundant public accessibility. Works by building the project to generate an index store, then constructing an in-memory dependency graph. Version 3.0 added significant improvements. Essential for codebase hygiene.
- **Loop phase:** verify (periodic cleanup, CI gate)
- **Install:**
  ```bash
  brew install periphery
  mint install peripheryapp/periphery
  ```
- **Claude Code integration:** Shell out to `periphery scan --setup` for interactive guided setup, then `periphery scan --format json` for structured output. Parse JSON results to identify dead code. Can integrate into CI with `periphery scan --strict` (non-zero exit on findings).
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS (runs on macOS and Linux)

### Tailor (Legacy)

- **Link:** [github.com/sleekbyte/tailor](https://github.com/sleekbyte/tailor)
- **Description:** Cross-platform static analyzer and linter for Swift. Written in Java. Supports Swift 2.x/3.x. **Effectively unmaintained** -- last meaningful updates targeted Swift 3.0. Not recommended for new projects; included for historical reference. SwiftLint has fully superseded it.
- **Loop phase:** verify
- **Install:** `brew install tailor` (if available)
- **Claude Code integration:** Not recommended. Use SwiftLint instead.
- **Platforms:** macOS, Linux, Windows (Java-based)

---

## Testing Frameworks (verify)

### Swift Testing (Apple)

- **Link:** [developer.apple.com/xcode/swift-testing](https://developer.apple.com/xcode/swift-testing/)
- **Description:** Apple's modern testing framework, introduced at WWDC24, shipping with Swift 6 and Xcode 16+. Uses `@Test` and `@Suite` macros for expressive, Swift-native test declarations. Parameterized tests, traits for configuration, parallel execution by default, full Swift Concurrency integration. Coexists with XCTest -- migrate incrementally. Does **not** yet support UI automation (`XCUIApplication`) or performance metrics (`XCTMetric`); use XCTest for those.
- **Loop phase:** verify
- **Install:**
  ```bash
  # Built into Swift 6+ toolchain / Xcode 16+
  # Import in test target:
  import Testing
  ```
- **Claude Code integration:** Shell out to `swift test` or `xcodebuild test`. Parse stdout for `@Test` results. Use `swift test --filter <pattern>` to run specific tests. JSON output available via `swift test --format json` (Swift 6.1+).
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS

### XCTest (Apple)

- **Link:** [developer.apple.com/documentation/xctest](https://developer.apple.com/documentation/xctest)
- **Description:** Apple's original testing framework. Provides unit testing (`XCTestCase`), UI testing (`XCUIApplication`), and performance testing (`XCTMetric`, `measure {}`). Mature, stable, universally supported. Still required for UI automation and performance benchmarks. Runs via `xcodebuild test` or `swift test`.
- **Loop phase:** verify
- **Install:**
  ```bash
  # Built into Xcode and Swift toolchain
  import XCTest
  ```
- **Claude Code integration:** Shell out to `xcodebuild test -scheme <scheme> -destination <dest>` or `swift test`. Use `-resultBundlePath` for structured results, then parse with `xcresulttool`. Use `xcodebuild test -only-testing:<target>/<class>/<method>` for targeted runs.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS

### Quick / Nimble

- **Link:** [github.com/Quick/Quick](https://github.com/Quick/Quick) | [github.com/Quick/Nimble](https://github.com/Quick/Nimble)
- **Description:** BDD-style testing framework (Quick) paired with a matcher framework (Nimble). Quick provides `describe`/`context`/`it` blocks inspired by RSpec. Nimble provides expressive matchers (`expect(x).to(equal(y))`). Quick 7.x and Nimble 14.x are current. Good for teams that prefer BDD-style test organization.
- **Loop phase:** verify
- **Install:**
  ```swift
  // Package.swift
  .package(url: "https://github.com/Quick/Quick", from: "7.0.0"),
  .package(url: "https://github.com/Quick/Nimble", from: "13.0.0")
  ```
- **Claude Code integration:** Tests run via standard `swift test` or `xcodebuild test`. No special CLI needed. Parse test output as usual.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS, Linux

### swift-snapshot-testing (Point-Free)

- **Link:** [github.com/pointfreeco/swift-snapshot-testing](https://github.com/pointfreeco/swift-snapshot-testing)
- **Description:** Snapshot testing library that captures and compares artifacts (images, text, JSON, custom formats). Supports Swift Testing (beta) and XCTest. Version 1.17+ adds `withSnapshotTesting` for scoped configuration. Extensible snapshot strategies for SwiftUI views, UIKit views, Codable values, and more. Essential for UI regression testing.
- **Loop phase:** verify
- **Install:**
  ```swift
  // Package.swift (add to test targets only)
  .package(url: "https://github.com/pointfreeco/swift-snapshot-testing", from: "1.17.0")
  ```
- **Claude Code integration:** Run via `swift test`. When snapshots fail, diffs are written to `__Snapshots__` directories. Shell out to compare or regenerate with `SNAPSHOT_TESTING_RECORD=1 swift test` (env var). Cannot visually inspect images from CLI, but text/JSON snapshots are diffable.
- **Platforms:** iOS, macOS, tvOS, Linux

### ViewInspector

- **Link:** [github.com/nalexn/ViewInspector](https://github.com/nalexn/ViewInspector)
- **Description:** Runtime introspection library for unit testing SwiftUI views. Traverses the compiled view hierarchy to inspect view structures, attributes, modifiers, and trigger callbacks. Two testing surfaces: "outside" (rendered structure) and "inside" (state and injected references). Version 0.10.x is current. Fills the gap left by Apple's lack of official SwiftUI unit testing support.
- **Loop phase:** verify
- **Install:**
  ```swift
  // Package.swift (add to test targets only)
  .package(url: "https://github.com/nalexn/ViewInspector", from: "0.10.0")
  ```
- **Claude Code integration:** Tests run via standard `swift test`. No special CLI. Write tests that traverse view hierarchy and assert on properties. Parse standard test output.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS, Linux

### swift-custom-dump (Point-Free)

- **Link:** [github.com/pointfreeco/swift-custom-dump](https://github.com/pointfreeco/swift-custom-dump)
- **Description:** Debugging and testing toolkit providing: `customDump()` for pretty-printing any value, `diff()` for visual diffs between values, and `XCTAssertNoDifference` / `expectNoDifference` (Swift Testing) for assertions with rich failure messages. Far superior to `XCTAssertEqual` for complex types. Swift 6 and Swift Testing compatible.
- **Loop phase:** verify (better test diagnostics)
- **Install:**
  ```swift
  // Package.swift
  .package(url: "https://github.com/pointfreeco/swift-custom-dump", from: "1.0.0")
  ```
- **Claude Code integration:** Use in test targets for better failure output. Run via `swift test`. The improved diff output in test failures makes diagnosing issues from CLI much easier.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS, Linux

---

## Code Generation (implement)

### Sourcery

- **Link:** [github.com/krzysztofzablocki/Sourcery](https://github.com/krzysztofzablocki/Sourcery)
- **Description:** Meta-programming code generator for Swift, built on SwiftSyntax. Uses Stencil, EJS, or Swift templates to generate boilerplate code -- mocks, equatable conformances, enum cases, lenses, and arbitrary patterns. Used in 40,000+ projects (Airbnb, Bumble, NYT). Version 2.3.x is current. Supports daemon mode for live regeneration. Helped push Apple toward derived conformances.
- **Loop phase:** implement (generate before build)
- **Install:**
  ```bash
  brew install sourcery
  mint install krzysztofzablocki/Sourcery
  ```
- **Claude Code integration:** Shell out to `sourcery --sources <path> --templates <path> --output <path>`. Use `--watch` for continuous regeneration during development. Use `--args` to pass template parameters. Parse generated files to verify output.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS (runs on macOS and Linux)

### SwiftGen

- **Link:** [github.com/SwiftGen/SwiftGen](https://github.com/SwiftGen/SwiftGen)
- **Description:** Generates type-safe Swift code for project resources: asset catalogs (images, colors, symbols, AR resources, data sets), localized strings, fonts, storyboards/XIBs, Core Data models, plists, JSON/YAML files, colors (from text/JSON/XML/.clr), and file/directory structures. Eliminates stringly-typed resource access. Version 6.6.x is current. Customizable via Stencil templates. Configuration via `swiftgen.yml`.
- **Loop phase:** implement (generate before build)
- **Install:**
  ```bash
  brew install swiftgen
  mint install SwiftGen/SwiftGen
  pod 'SwiftGen', '~> 6.0'
  ```
- **Claude Code integration:** Shell out to `swiftgen config run` (uses `swiftgen.yml`) or `swiftgen <subcommand>` for individual resource types. Use `swiftgen config generate-xcfilelist` to generate input/output file lists for Xcode build phases.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS (runs on macOS)

### Needle (Uber)

- **Link:** [github.com/uber/needle](https://github.com/uber/needle)
- **Description:** Compile-time safe dependency injection framework from Uber. Generates DI code during compilation so missing dependencies fail at build time, not runtime. Core concepts: dependency protocols, components, and child component instantiation. Designed for large-scale apps with complex dependency graphs. Requires both `NeedleFoundation` framework and a code generator binary.
- **Loop phase:** implement (generate DI code before build)
- **Install:**
  ```bash
  brew install needle
  # Or add NeedleFoundation as SPM dependency
  .package(url: "https://github.com/uber/needle", from: "0.24.0")
  ```
- **Claude Code integration:** Shell out to the needle code generator as a build phase. Verify compile-time safety by running `swift build` after generation. Not directly useful as a standalone CLI tool; integrated into the build pipeline.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS

### swift-dependencies (Point-Free)

- **Link:** [github.com/pointfreeco/swift-dependencies](https://github.com/pointfreeco/swift-dependencies)
- **Description:** Lightweight dependency management library inspired by SwiftUI's environment. Uses `@Dependency` macro and Swift Task Locals for context-propagated dependency injection. Version 1.11.x is current. Supports Swift 6.1's `TestScoping` for reliable test injection. Not a code generator per se, but provides the `@DependencyClient` macro for generating dependency interfaces.
- **Loop phase:** implement (architecture pattern)
- **Install:**
  ```swift
  // Package.swift
  .package(url: "https://github.com/pointfreeco/swift-dependencies", from: "1.0.0")
  ```
- **Claude Code integration:** Not a CLI tool. Used as a library dependency. Claude Code can scaffold `@Dependency` and `@DependencyClient` declarations when generating new features.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS, Linux

---

## Package Management (implement)

### Swift Package Manager (SPM)

- **Link:** [github.com/swiftlang/swift-package-manager](https://github.com/swiftlang/swift-package-manager) | [swift.org/documentation/package-manager](https://www.swift.org/documentation/package-manager/)
- **Description:** Apple's official package manager, built into the Swift toolchain and Xcode. Defines dependencies in `Package.swift`. Resolves versions via `Package.resolved`. Swift 6.1+ adds strict mode for tighter version matching, dry-run updates, dependency graph visualization, and package info commands. The standard for modern Swift projects.
- **Loop phase:** implement
- **Key CLI commands:**
  ```bash
  swift package init --type executable|library
  swift build
  swift test
  swift run <executable>
  swift package resolve
  swift package update
  swift package show-dependencies --format json
  swift package show-dependencies --format dot    # dependency graph
  swift package clean
  swift package reset                             # removes .build + Package.resolved
  swift package purge-cache
  swift package plugin <command>                  # run command plugins
  ```
- **Claude Code integration:** Direct shell-out to all commands above. `swift package show-dependencies --format json` provides structured dependency data. `swift build 2>&1` captures build errors. `swift test --filter <pattern>` for targeted testing.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS, Linux, Windows

### CocoaPods (Legacy -- Sunsetting)

- **Link:** [cocoapods.org](https://cocoapods.org/) | [github.com/CocoaPods/CocoaPods](https://github.com/CocoaPods/CocoaPods)
- **Description:** Legacy dependency manager for Swift and Objective-C. **Trunk goes read-only December 2, 2026.** No new pods can be published after that date. Google dropping CocoaPods support for iOS SDKs after Q2 2026. Migrate to SPM. Still functional for existing projects during transition period.
- **Loop phase:** implement (legacy maintenance only)
- **Install:**
  ```bash
  sudo gem install cocoapods
  pod install
  pod update
  ```
- **Claude Code integration:** Shell out to `pod install`, `pod update`, `pod outdated`. Parse `Podfile.lock` for dependency analysis. **Prioritize migrating to SPM.**
- **Platforms:** iOS, macOS, watchOS, tvOS

### Mint

- **Link:** [github.com/yonaskolb/Mint](https://github.com/yonaskolb/Mint)
- **Description:** Package manager for installing and running Swift CLI tools. Installs executables from any Swift package with an executable target. Supports multiple versions side-by-side. Central cache. Version 0.18.x is current. Ideal for managing project-specific tool versions (SwiftLint, SwiftFormat, Sourcery, etc.) via a `Mintfile`.
- **Loop phase:** implement (tool management)
- **Install:**
  ```bash
  brew install mint
  ```
- **Key commands:**
  ```bash
  mint install <repo>@<version>    # install a tool
  mint run <repo> <command>        # run without global install
  mint bootstrap                   # install all tools from Mintfile
  mint list                        # list installed tools
  ```
- **Claude Code integration:** Shell out to `mint run <tool> <args>` for reproducible tool execution. Use `Mintfile` for version-pinned tool management across the team. `mint bootstrap` ensures all tools are available.
- **Platforms:** macOS, Linux

---

## Static Analysis (verify)

### SwiftLint Analyzer Mode

- **Link:** [github.com/realm/SwiftLint](https://github.com/realm/SwiftLint) (same tool, different mode)
- **Description:** SwiftLint's `analyze` command performs deeper static analysis using the full type-checked AST from a clean build. Analyzer rules are a separate opt-in rule set (enable via `analyzer_rules` in `.swiftlint.yml`). Slower than lint mode but catches issues that require type information. Requires passing a compiler log from a clean (non-incremental) build.
- **Loop phase:** verify (CI, periodic deep analysis)
- **Usage:**
  ```bash
  # 1. Do a clean build and capture log
  xcodebuild clean build -scheme MyApp > build_log.txt 2>&1
  # 2. Run analyzer
  swiftlint analyze --compiler-log-path build_log.txt
  ```
- **Claude Code integration:** Two-step process: capture build log, then run analyzer. Parse output for type-aware violations. Best run in CI rather than on every save.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS

### Semgrep (Swift GA)

- **Link:** [semgrep.dev/docs/languages/swift](https://semgrep.dev/docs/languages/swift)
- **Description:** General-purpose static analysis tool with GA (General Availability) Swift support. 57 Pro rules covering security vulnerability classes (injection, auth, crypto, data exposure). Community Edition supports custom rule writing with Swift pattern matching. Supply Chain scanning supports SPM lockfiles. Pro Engine provides framework-specific analysis not available in CE.
- **Loop phase:** verify (security scanning, CI gate)
- **Install:**
  ```bash
  pip install semgrep       # or brew install semgrep
  ```
- **Usage:**
  ```bash
  semgrep scan --config auto .                          # auto-detect rules
  semgrep scan --config p/swift .                       # Swift-specific rules
  semgrep scan --config r/swift.lang.security .         # security rules
  ```
- **Claude Code integration:** Shell out to `semgrep scan --json --config auto <path>` for structured output. Write custom `.semgrep.yml` rules for project-specific patterns. MCP integration available via Semgrep plugin for real-time scanning.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS (runs on macOS, Linux)

### SonarQube (Swift)

- **Link:** [sonarsource.com/knowledge/languages/swift](https://www.sonarsource.com/knowledge/languages/swift/)
- **Description:** Enterprise code quality platform with native Swift analysis. Built directly in Swift using the official compiler and parser. Supports all Swift versions through 6.2. Available in Developer Edition and above (not Community). Open-source alternatives: [sonar-apple](https://github.com/insideapp-oss/sonar-apple) (SonarQube 9.9+) and [sonar-swift](https://github.com/Idean/sonar-swift) (wraps SwiftLint/Tailor).
- **Loop phase:** verify (CI/CD quality gate)
- **Install:** Server-based; configure scanner in CI pipeline
- **Claude Code integration:** Not directly CLI-invocable. Use `sonar-scanner` CLI in CI. Results viewed via web dashboard. For local analysis, SwiftLint + Semgrep provide better CLI integration.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS

### Swift AST Explorer

- **Link:** [swift-ast-explorer.com](https://swift-ast-explorer.com/) | [github.com/SwiftFiddle/swift-ast-explorer](https://github.com/SwiftFiddle/swift-ast-explorer)
- **Description:** Web-based tool for visualizing the Abstract Syntax Tree of Swift source code. Write Swift on the left, explore the syntax tree on the right. Invaluable for understanding SwiftSyntax node types when writing macros, Sourcery templates, or custom SwiftLint rules. Apache 2.0 licensed.
- **Loop phase:** plan (understanding code structure)
- **Install:** Web-based, no install needed
- **Claude Code integration:** Not CLI-invocable. Reference tool for planning. For programmatic AST access, use SwiftSyntax directly.
- **Platforms:** Web (browser-based)

---

## Profiling & Performance (verify)

### Instruments / xctrace

- **Link:** [developer.apple.com/instruments](https://developer.apple.com/instruments/) | [man page: xctrace(1)](https://keith.github.io/xcode-man-pages/xctrace.1.html)
- **Description:** Apple's profiling suite. The `xctrace` CLI provides full access to Instruments from the command line. Records traces for CPU, memory, SwiftUI view updates, Swift concurrency (Tasks, Actors), animation hitches, disk I/O, network, and more. Xcode 16+ recommends `--instrument` over `--template` for reliable export. Outputs `.trace` files analyzable in Instruments.app or via `xctrace export`.
- **Loop phase:** verify (performance profiling)
- **Key commands:**
  ```bash
  xctrace record --device <udid> --instrument "Time Profiler" --launch <app>
  xctrace record --instrument "SwiftUI" --attach <pid>
  xctrace export --input recording.trace --output data.xml
  xctrace list instruments    # list available instruments
  xctrace list devices        # list available devices
  ```
- **Claude Code integration:** Shell out to `xctrace record` for automated profiling runs. Export to XML with `xctrace export` and parse results. Useful for CI performance regression detection. MCP servers exist for Instruments integration (see [instruments-profiling on Smithery](https://smithery.ai/skills/steipete/instruments-profiling)).
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS

### Memory Graph Debugger

- **Link:** [developer.apple.com/documentation/xcode/gathering-information-about-memory-use](https://developer.apple.com/documentation/xcode/gathering-information-about-memory-use)
- **Description:** Xcode tool that captures a snapshot of the object graph to detect retain cycles, leaked allocations, and abandoned memory. Available via Xcode's Debug navigator or `leaks` and `heap` command-line tools. Captures `.memgraph` files for offline analysis.
- **Loop phase:** verify (memory debugging)
- **Key commands:**
  ```bash
  leaks --process=<pid>                    # detect leaks in running process
  leaks <memgraph_file>                    # analyze captured memory graph
  heap <pid>                               # heap snapshot
  vmmap <pid>                              # virtual memory map
  malloc_history <pid> <address>           # allocation history
  ```
- **Claude Code integration:** Shell out to `leaks --process=<pid> --outputGraph=leak.memgraph` for automated leak detection. Parse `leaks` text output for CI integration. Combine with `xcrun simctl` for simulator-based testing.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS

### os_signpost / OSSignposter

- **Link:** [developer.apple.com/documentation/os/ossignposter](https://developer.apple.com/documentation/os/ossignposter)
- **Description:** Apple's instrumentation API for marking performance-critical code sections. Place signpost intervals around operations to measure duration in Instruments. Three types: event signposts (point-in-time), interval signposts (begin/end duration), and breadcrumbs (lightweight tracking). Integrated with the unified logging system. OSSignposter is the modern Swift API (replacing C-style `os_signpost`).
- **Loop phase:** implement (instrument code), verify (measure in Instruments)
- **Install:** Built into the OS framework -- `import os`
- **Claude Code integration:** Not a CLI tool. Claude Code can add signpost instrumentation to source code, then use `xctrace` to record and analyze the resulting data. Generate boilerplate signpost code on request.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS

### MetricKit

- **Link:** [developer.apple.com/documentation/metrickit](https://developer.apple.com/documentation/metrickit)
- **Description:** Apple framework for collecting on-device performance and diagnostic data from production apps. Provides `MXMetricPayload` (CPU, memory, disk, network, app launch, animation hitches) and `MXDiagnosticPayload` (crashes, hangs, disk writes). Data delivered daily via `MXMetricManagerSubscriber`. Essential for production performance monitoring.
- **Loop phase:** verify (production monitoring)
- **Install:** Built into iOS 13+ / macOS 12+ -- `import MetricKit`
- **Claude Code integration:** Not a CLI tool. Claude Code can scaffold MetricKit subscriber code and payload processing. Production data analysis happens server-side.
- **Platforms:** iOS, macOS (iPadOS, watchOS 9+, visionOS)

---

## Documentation (implement)

### DocC (Swift-DocC)

- **Link:** [github.com/swiftlang/swift-docc](https://github.com/swiftlang/swift-docc) | [swift.org/documentation/docc](https://www.swift.org/documentation/docc/)
- **Description:** Apple's documentation compiler for Swift frameworks and packages. Generates rich API reference documentation and interactive tutorials from doc comments and markdown articles. Powers most of Apple's developer documentation. Supports customizable symbol access levels, C/C++/Objective-C targets, and static site hosting. swift-docc-plugin integrates with SPM.
- **Loop phase:** implement (write docs alongside code)
- **Install:**
  ```bash
  # Built into Swift 6+ toolchain
  # Add plugin for SPM projects:
  .package(url: "https://github.com/swiftlang/swift-docc-plugin", from: "1.4.0")
  ```
- **Key commands:**
  ```bash
  swift package generate-documentation                   # generate docs
  swift package generate-documentation --hosting-base-path <path>
  swift package preview-documentation                    # local preview server
  swift package generate-documentation --output-path docs  # export
  ```
- **Claude Code integration:** Shell out to `swift package generate-documentation` to build docs. Preview with `swift package preview-documentation --port 8080`. Verify doc coverage by checking build warnings for undocumented symbols (use `--warnings-as-errors`).
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS, Linux

### swift-docc-plugin

- **Link:** [github.com/swiftlang/swift-docc-plugin](https://github.com/swiftlang/swift-docc-plugin)
- **Description:** SPM command plugin that integrates Swift-DocC with Swift Package Manager. Enables `swift package generate-documentation` and `swift package preview-documentation` commands. Version 1.4.x is current. Supports generating documentation for multiple targets, customizing access levels, and exporting for static hosting (GitHub Pages, etc.).
- **Loop phase:** implement
- **Install:**
  ```swift
  // Package.swift
  .package(url: "https://github.com/swiftlang/swift-docc-plugin", from: "1.4.0")
  ```
- **Claude Code integration:** Same CLI as DocC above. The plugin is the bridge between SPM and DocC.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS, Linux

### jazzy (Legacy)

- **Link:** [github.com/realm/jazzy](https://github.com/realm/jazzy)
- **Description:** Ruby-based documentation generator that produces Apple-style reference docs for Swift and Objective-C. Uses Clang/SourceKit AST or compiled module symbol graphs. Still maintained (last update October 2025) but superseded by DocC for new projects. Useful for projects that need HTML docs without adopting DocC's format, or for Objective-C-heavy codebases.
- **Loop phase:** implement
- **Install:**
  ```bash
  sudo gem install jazzy
  # or
  [sudo] gem install jazzy
  ```
- **Key commands:**
  ```bash
  jazzy --module MyFramework                  # generate docs
  jazzy --module MyFramework --swift-build-tool spm
  jazzy --sourcekitten-sourcefile data.json   # from pre-generated data
  ```
- **Claude Code integration:** Shell out to `jazzy --module <name>`. Output is HTML in `docs/` directory. Less structured output than DocC but simpler setup for legacy projects.
- **Platforms:** macOS (generates docs for all Apple platforms)

---

## Dependency Security (verify)

### Snyk (Swift/iOS)

- **Link:** [docs.snyk.io/supported-languages/swift-and-objective-c](https://docs.snyk.io/supported-languages/supported-languages-list/swift-and-objective-c)
- **Description:** Developer security platform with SCA (Software Composition Analysis) and SAST for Swift. SCA scans CocoaPods (`Podfile.lock`) and SPM (`Package.resolved`) dependencies for known vulnerabilities. SAST (Snyk Code) identifies security issues in Swift source code including grpc-swift. Uses `swift package show-dependencies` for SPM dependency graph construction. Requires Swift 3.0+.
- **Loop phase:** verify (security scanning, CI gate)
- **Install:**
  ```bash
  npm install -g snyk    # or brew install snyk
  snyk auth              # authenticate
  ```
- **Key commands:**
  ```bash
  snyk test                         # scan dependencies for vulnerabilities
  snyk code test                    # SAST scan of source code
  snyk monitor                      # continuous monitoring
  snyk test --all-projects          # scan all projects in directory
  ```
- **Claude Code integration:** Shell out to `snyk test --json` for structured vulnerability data. `snyk code test --json` for SAST results. Parse JSON to surface actionable security findings. Integrate into CI with `snyk test --severity-threshold=high`.
- **Platforms:** iOS, macOS (scans projects targeting all Apple platforms)

### Semgrep Supply Chain

- **Link:** [semgrep.dev/products/product-updates/swift-support](https://semgrep.dev/products/product-updates/swift-support/)
- **Description:** Semgrep's supply chain scanning supports Swift via SPM lockfile analysis (`Package.resolved`). Detects known vulnerabilities in third-party dependencies. Part of the broader Semgrep platform -- combines with Semgrep Code for both dependency and source-level security scanning.
- **Loop phase:** verify (dependency security)
- **Install:**
  ```bash
  pip install semgrep    # or brew install semgrep
  ```
- **Usage:**
  ```bash
  semgrep ci --supply-chain    # supply chain scan in CI
  ```
- **Claude Code integration:** Shell out to `semgrep ci --supply-chain --json` for structured output. Combines with source scanning in a single tool.
- **Platforms:** iOS, macOS (scans SPM-based projects)

### OWASP Dependency-Check (Swift Analyzer)

- **Link:** [jeremylong.github.io/DependencyCheck/analyzers/swift.html](https://jeremylong.github.io/DependencyCheck/analyzers/swift.html)
- **Description:** Open-source SCA tool with an experimental Swift Package Manager analyzer. Scans `Package.swift` to identify dependencies and map them to known CVEs via the NVD (National Vulnerability Database). Free and open-source alternative to commercial SCA tools. Java-based CLI.
- **Loop phase:** verify (dependency security)
- **Install:**
  ```bash
  brew install dependency-check
  ```
- **Usage:**
  ```bash
  dependency-check --project "MyApp" --scan . --enableExperimental
  ```
- **Claude Code integration:** Shell out to `dependency-check --scan . --format JSON --enableExperimental` for structured output. Parse JSON report for vulnerabilities. Note: Swift analyzer is experimental -- may have false positives/negatives.
- **Platforms:** macOS, Linux (scans SPM projects)

### Socket.dev

- **Link:** [socket.dev](https://socket.dev/)
- **Description:** Supply chain security platform that proactively detects malicious and compromised packages. **Does not currently support Swift/SPM.** Covers JavaScript (npm), Python (PyPI), Go, and Rust ecosystems. Included here for awareness -- may add Swift support in the future as it expands language coverage. Monitor their announcements.
- **Loop phase:** N/A (no Swift support yet)
- **Claude Code integration:** N/A
- **Platforms:** N/A for Swift

---

## Tool Comparison Quick Reference

| Tool | Category | Install | CLI-Friendly | Active (2026) | Recommended |
|------|----------|---------|:------------:|:--------------:|:-----------:|
| SwiftLint | Lint | brew/mint/spm | Yes | Yes | **Yes** |
| SwiftFormat | Format | brew/mint | Yes | Yes | **Yes** |
| swift-format | Format | toolchain | Yes | Yes | Yes |
| Periphery | Dead code | brew/mint | Yes | Yes | **Yes** |
| Tailor | Lint | brew | Yes | No | No |
| Swift Testing | Test | toolchain | Yes | Yes | **Yes** |
| XCTest | Test | toolchain | Yes | Yes | **Yes** |
| Quick/Nimble | Test | spm | Yes | Yes | Optional |
| swift-snapshot-testing | Test | spm | Yes | Yes | **Yes** |
| ViewInspector | Test | spm | Yes | Yes | **Yes** |
| swift-custom-dump | Test | spm | Yes | Yes | **Yes** |
| Sourcery | Codegen | brew/mint | Yes | Yes | **Yes** |
| SwiftGen | Codegen | brew/mint | Yes | Yes | **Yes** |
| Needle | DI | brew/spm | Partial | Yes | Situational |
| swift-dependencies | DI | spm | No (library) | Yes | **Yes** |
| SPM | Packages | toolchain | Yes | Yes | **Yes** |
| CocoaPods | Packages | gem | Yes | Sunsetting | Migrate away |
| Mint | Tool mgmt | brew | Yes | Yes | **Yes** |
| Semgrep | Security/SAST | pip/brew | Yes | Yes | **Yes** |
| SonarQube | Quality | server | Partial | Yes | Enterprise |
| xctrace | Profiling | toolchain | Yes | Yes | **Yes** |
| DocC | Docs | toolchain/spm | Yes | Yes | **Yes** |
| jazzy | Docs | gem | Yes | Maintenance | Legacy |
| Snyk | Security/SCA | npm/brew | Yes | Yes | **Yes** |

---

## Sources

- [SwiftLint - GitHub](https://github.com/realm/SwiftLint)
- [SwiftFormat - GitHub](https://github.com/nicklockwood/SwiftFormat)
- [swift-format - GitHub](https://github.com/swiftlang/swift-format)
- [Periphery - GitHub](https://github.com/peripheryapp/periphery)
- [Swift Testing - Apple Developer](https://developer.apple.com/xcode/swift-testing/)
- [Quick - GitHub](https://github.com/Quick/Quick)
- [Nimble - GitHub](https://github.com/Quick/Nimble)
- [swift-snapshot-testing - GitHub](https://github.com/pointfreeco/swift-snapshot-testing)
- [ViewInspector - GitHub](https://github.com/nalexn/ViewInspector)
- [swift-custom-dump - GitHub](https://github.com/pointfreeco/swift-custom-dump)
- [Sourcery - GitHub](https://github.com/krzysztofzablocki/Sourcery)
- [SwiftGen - GitHub](https://github.com/SwiftGen/SwiftGen)
- [Needle - GitHub](https://github.com/uber/needle)
- [swift-dependencies - GitHub](https://github.com/pointfreeco/swift-dependencies)
- [Swift Package Manager - GitHub](https://github.com/swiftlang/swift-package-manager)
- [CocoaPods Deprecation Notice](https://dev.to/surhidamatya/cocoapods-is-going-read-only-what-ios-developers-need-to-know-19j8)
- [Mint - GitHub](https://github.com/yonaskolb/Mint)
- [Semgrep Swift GA](https://semgrep.dev/docs/languages/swift)
- [SonarQube Swift](https://www.sonarsource.com/knowledge/languages/swift/)
- [Swift AST Explorer](https://swift-ast-explorer.com/)
- [xctrace man page](https://keith.github.io/xcode-man-pages/xctrace.1.html)
- [OSSignposter - Apple](https://developer.apple.com/documentation/os/ossignposter)
- [MetricKit - Apple](https://developer.apple.com/documentation/metrickit)
- [DocC - swift.org](https://www.swift.org/documentation/docc/)
- [swift-docc-plugin - GitHub](https://github.com/swiftlang/swift-docc-plugin)
- [jazzy - GitHub](https://github.com/realm/jazzy)
- [Snyk Swift Docs](https://docs.snyk.io/supported-languages/supported-languages-list/swift-and-objective-c)
- [Semgrep Supply Chain Swift](https://semgrep.dev/products/product-updates/swift-support/)
- [OWASP Dependency-Check Swift](https://jeremylong.github.io/DependencyCheck/analyzers/swift.html)
- [Socket.dev](https://socket.dev/)
- [Tailor - GitHub](https://github.com/sleekbyte/tailor)

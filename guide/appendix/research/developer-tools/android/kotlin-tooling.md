---
id: e1707869-629b-4732-b372-9fec499f92b6
title: Kotlin & Android Development Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/android/kotlin-tooling
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Kotlin & Android Development Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Kotlin & Android Development Tools

**Date:** 2026-03-29
**Context:** Kotlin/Android development tools that integrate with Claude Code for the plan/implement/verify loop.

---

## Linters & Formatters (implement/verify)

### [ktlint](https://github.com/pinterest/ktlint) — Pinterest

**What it does:** Anti-bikeshedding Kotlin linter and formatter. Captures Kotlin coding conventions and the Android Kotlin Style Guide with zero configuration required. Auto-fixes most violations.

**Current version:** 1.8.0 (Gradle plugin 12.2.0)

**Loop phase:** implement (format-on-save), verify (CI lint gate)

**Install:**
```kotlin
// build.gradle.kts — via ktlint-gradle plugin
plugins {
    id("org.jlleitschuh.gradle.ktlint") version "12.2.0"
}
```
```bash
# Standalone CLI (Homebrew)
brew install ktlint
```

**Key CLI commands:**
```bash
ktlint                          # Check all .kt/.kts files recursively
ktlint --format                 # Auto-fix violations
ktlint "src/**/*.kt"            # Check specific path pattern
ktlint --baseline=baseline.xml  # Generate/check against baseline
./gradlew ktlintCheck           # Gradle task — check
./gradlew ktlintFormat          # Gradle task — auto-fix
```

**Claude Code integration:** Shell out to `ktlint --format` or `./gradlew ktlintFormat` after writing Kotlin files. Parse stdout for remaining violations. Standalone JAR works without Gradle context.

---

### [detekt](https://detekt.dev/) — detekt maintainers

**What it does:** Static code analysis for Kotlin. Finds code smells, complexity issues, naming violations, and style problems. Highly configurable rule engine with 200+ built-in rules. Supports HTML, Markdown, SARIF, and XML reports.

**Current version:** 1.23.x (see [releases](https://github.com/detekt/detekt/releases))

**Loop phase:** verify (static analysis gate)

**Install:**
```kotlin
// build.gradle.kts
plugins {
    id("io.gitlab.arturbosch.detekt") version "1.23.7"
}
```
```bash
# Standalone CLI (Homebrew)
brew install detekt
```

**Key CLI commands:**
```bash
detekt --input src/ --config detekt.yml   # Analyze with custom config
detekt --generate-config                   # Export default config as detekt.yml
detekt --baseline baseline.xml             # Generate baseline for existing issues
./gradlew detekt                           # Gradle task
./gradlew detektBaseline                   # Generate baseline via Gradle
```

**Claude Code integration:** Shell out to `detekt --input src/` or `./gradlew detekt`. Parse SARIF/XML output for structured findings. Use `--generate-config` to bootstrap a config file, then customize rule thresholds. Detekt findings import into SonarQube via the sonar-detekt plugin.

---

### [ktfmt](https://facebook.github.io/ktfmt/) — Meta

**What it does:** Opinionated Kotlin code formatter based on google-java-format. Deterministic output regardless of input formatting. Non-customizable by design to enforce consistency. 40% faster than ktlint in large codebases (per Square's benchmarks on 60,000+ files).

**Current version:** 0.62

**Loop phase:** implement (format-on-save)

**Install:**
```kotlin
// build.gradle.kts — via ktfmt-gradle plugin
plugins {
    id("com.ncorti.ktfmt.gradle") version "0.22.0"
}
```
```bash
# Standalone (Homebrew)
brew install ktfmt
```

**Key CLI commands:**
```bash
ktfmt src/**/*.kt                     # Format files
ktfmt --kotlinlang-style src/**/*.kt  # Use Kotlin style (vs Google style)
ktfmt --dry-run src/**/*.kt           # Check without modifying
./gradlew ktfmtCheck                  # Gradle check
./gradlew ktfmtFormat                 # Gradle format
```

**Claude Code integration:** Shell out to `ktfmt` after generating Kotlin files. The `--dry-run` flag works well for verify-phase checks. Choose one formatter (ktfmt OR ktlint) per project, not both.

---

### [diktat](https://diktat.saveourtool.com/) — SaveOurTool (originally Huawei)

**What it does:** Strict coding standard for Kotlin with 100+ checkers built on the ktlint rule engine. Focuses on code smells, style issues, and bugs. Includes auto-fixing capabilities.

**Current version:** 2.0.0

**Loop phase:** verify (stricter style enforcement)

**Install:**
```kotlin
// build.gradle.kts
plugins {
    id("com.saveourtool.diktat") version "2.0.0"
}
```

**Key CLI commands:**
```bash
./gradlew diktatCheck    # Check
./gradlew diktatFix      # Auto-fix
```

**Claude Code integration:** Shell out to Gradle tasks. Diktat is stricter than ktlint and targets teams wanting enforced conventions beyond formatting. Useful when a project needs Huawei-style coding standards or more opinionated checks.

---

### [Android Lint](https://developer.android.com/studio/write/lint) — Google (built-in)

**What it does:** Built-in static analysis tool for Android projects. Checks for structural issues, performance problems, accessibility, internationalization, security vulnerabilities, and correctness. Supports custom rule authoring. AGP version + 23 = Lint version (e.g., AGP 8.x = Lint 31.x).

**Loop phase:** verify (Android-specific correctness)

**Install:** Included with Android Gradle Plugin — no separate install needed.

**Key CLI commands:**
```bash
./gradlew lint                     # Run all lint checks
./gradlew lintDebug                # Lint specific variant
./gradlew lintRelease              # Lint release variant
./gradlew lint --continue          # Don't stop on first failure
```

**Configuration (build.gradle.kts):**
```kotlin
android {
    lint {
        abortOnError = true
        warningsAsErrors = true
        baseline = file("lint-baseline.xml")
        htmlReport = true
    }
}
```

**Claude Code integration:** Shell out to `./gradlew lint`. Parse the HTML or XML report at `build/reports/lint-results*.html`. Use baseline files to suppress pre-existing issues. Custom lint rules can be authored as separate modules and loaded via `--lint-rule-jars` or `ANDROID_LINT_JARS` env var.

---

## Testing Frameworks (verify)

### [JUnit 5](https://junit.org/junit5/) — JUnit Team

**What it does:** The standard test framework for JVM projects. JUnit Jupiter provides annotations (`@Test`, `@BeforeEach`, `@ParameterizedTest`), lifecycle callbacks, and an extension model. Recent releases add Kotlin-friendly features: top-level assertions with contracts, `Sequence` parameter sources, and native `suspend` test support.

**Current version:** 5.11.x (Jupiter); JUnit 6 preview available

**Loop phase:** verify

**Install:**
```kotlin
// build.gradle.kts
dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter:5.11.4")
}
tasks.withType<Test> {
    useJUnitPlatform()
}
```

**Key CLI commands:**
```bash
./gradlew test                        # Run all tests
./gradlew test --tests "*.MyTest"     # Run specific test class
./gradlew test --rerun-tasks          # Force re-run (ignore up-to-date)
./gradlew test --continue             # Run all even if some fail
```

**Claude Code integration:** Shell out to `./gradlew test`. Parse XML reports at `build/test-results/`. JUnit 5 is the default runner for Gradle. Combine with `kotlinx-coroutines-test` for suspend function testing.

---

### [Kotest](https://kotest.io/) — Kotest Team

**What it does:** Multiplatform Kotlin test framework with 10+ testing styles (FunSpec, BehaviorSpec, StringSpec, etc.), 350+ built-in assertions, integrated property testing (100+ generators with shrinking), and data-driven testing (built into core since 6.0). First-class coroutine support.

**Current version:** 6.x (property testing and data-driven testing merged into core)

**Loop phase:** verify

**Install:**
```kotlin
// build.gradle.kts
dependencies {
    testImplementation("io.kotest:kotest-runner-junit5:6.0.0.M1")
    testImplementation("io.kotest:kotest-assertions-core:6.0.0.M1")
    testImplementation("io.kotest:kotest-property:6.0.0.M1")
}
```

**Claude Code integration:** Runs via JUnit Platform, so `./gradlew test` works. Kotest's property testing is valuable for generating edge cases Claude Code can't anticipate. Data-driven tests let Claude Code produce table-driven test specs efficiently.

---

### [MockK](https://mockk.io/) — MockK Team

**What it does:** Kotlin-native mocking library. Handles final classes (default in Kotlin), objects, companion objects, extension functions, top-level functions, and coroutines (`coEvery`/`coVerify`) without ceremony. Annotations: `@MockK`, `@RelaxedMockK`, `@InjectMockKs`. Integrates with JUnit 5, Kotest, and Spring (via SpringMockK).

**Current version:** 1.14.x (latest release January 2026)

**Loop phase:** verify (test doubles)

**Install:**
```kotlin
// build.gradle.kts
dependencies {
    testImplementation("io.mockk:mockk:1.14.5")
    androidTestImplementation("io.mockk:mockk-android:1.14.5")
}
```

**Limitations:** Cannot mock inline functions. Some spy/static scenarios need JVM `--add-opens` flags.

**Claude Code integration:** No CLI — used as a test dependency. Claude Code writes MockK-based tests and runs them via `./gradlew test`. MockK's DSL is concise enough for AI-generated test code.

---

### [Turbine](https://github.com/cashapp/turbine) — Cash App

**What it does:** Small testing library for `kotlinx.coroutines` Flow. Converts push-based Flows into pull-based suspend functions for straightforward assertion. Default 3-second timeout on awaits. Supports `awaitItem()`, `awaitError()`, `awaitComplete()`, `skipItems()`, and `cancelAndIgnoreRemainingEvents()`.

**Current version:** 1.2.1

**Loop phase:** verify (Flow testing)

**Install:**
```kotlin
// build.gradle.kts
dependencies {
    testImplementation("app.cash.turbine:turbine:1.2.1")
}
```

**Usage example:**
```kotlin
@Test
fun testFlow() = runTest {
    flowOf("one", "two").test {
        assertEquals("one", awaitItem())
        assertEquals("two", awaitItem())
        awaitComplete()
    }
}
```

**Claude Code integration:** No CLI — test dependency only. Claude Code writes Turbine-based Flow tests and runs via `./gradlew test`. Essential for testing ViewModels that expose `StateFlow`/`SharedFlow`.

---

### [kotlin-test](https://kotlinlang.org/api/kotlin-test/) — JetBrains

**What it does:** Official Kotlin multiplatform test library. Provides platform-agnostic annotations (`@Test`, `@BeforeTest`) and assertions (`assertEquals`, `assertTrue`, `assertFailsWith`). Thin abstraction over JUnit (JVM), XCTest (native), and Jasmine/Mocha (JS).

**Current version:** Ships with Kotlin stdlib (matches Kotlin version)

**Loop phase:** verify

**Install:**
```kotlin
// build.gradle.kts
dependencies {
    testImplementation(kotlin("test"))
}
```

**Claude Code integration:** Best for Kotlin Multiplatform projects where JUnit is not available on all targets. Claude Code writes tests using `kotlin.test` annotations and assertions, runs via `./gradlew test`. Assertions are simpler than Kotest but fully cross-platform.

---

### [Robolectric](https://robolectric.org/) — Google

**What it does:** Runs Android unit tests on the JVM without an emulator. Simulates Android framework APIs (Activities, Views, Resources, SQLite) via "shadows." Supports API levels 23-36 (Marshmallow through Baklava). Tests run ~10x faster than emulator tests.

**Current version:** 4.16

**Loop phase:** verify (fast Android unit tests)

**Install:**
```kotlin
// build.gradle.kts
dependencies {
    testImplementation("org.robolectric:robolectric:4.16")
}
```

**Key commands:**
```bash
./gradlew testDebugUnitTest    # Run unit tests (includes Robolectric)
```

**Claude Code integration:** Shell out to `./gradlew testDebugUnitTest`. Robolectric tests look like regular JUnit tests but can inflate layouts, interact with Views, and test Android lifecycle. Claude Code can write Robolectric tests without needing a running emulator.

---

## Code Generation (implement)

### [KSP](https://github.com/google/ksp) — Google (Kotlin Symbol Processing)

**What it does:** Kotlin-first annotation processing API. Analyzes Kotlin code directly (not Java stubs) for up to 2x faster builds than kapt. KSP2 is the default since early 2025. KSP1 is deprecated and incompatible with Kotlin 2.3+. Used by Room, Hilt, Moshi, and most modern Kotlin libraries.

**Current version:** 2.3.6 (tracks Kotlin version: `<kotlin-version>-<ksp-version>`)

**Loop phase:** implement (compile-time code generation)

**Install:**
```kotlin
// build.gradle.kts
plugins {
    id("com.google.devtools.ksp") version "2.1.20-1.0.32"
}
dependencies {
    ksp("com.example:my-processor:1.0.0")
}
```

**Key commands:**
```bash
./gradlew kspKotlin                 # Run KSP processors
./gradlew kspDebugKotlin            # Android debug variant
```

**Claude Code integration:** KSP runs automatically during `./gradlew build`. Claude Code should prefer KSP over kapt in all new projects. Generated sources appear in `build/generated/ksp/`. If a build fails with annotation processing errors, check KSP output.

---

### [kapt](https://kotlinlang.org/docs/kapt.html) — JetBrains (maintenance mode)

**What it does:** Kotlin Annotation Processing Tool. Generates Java stubs from Kotlin code, then runs Java annotation processors against those stubs. Slower than KSP because of the stub generation step. Now in maintenance mode — migrate to KSP when processors support it.

**Loop phase:** implement (legacy annotation processing)

**Install:**
```kotlin
// build.gradle.kts
plugins {
    kotlin("kapt")
}
dependencies {
    kapt("com.example:my-processor:1.0.0")
}
```

**Claude Code integration:** Only use when a library has no KSP support. `./gradlew kaptDebugKotlin` runs processors. K2 kapt enabled by default in Kotlin 2.1.20+. Migration guide: [developer.android.com/build/migrate-to-ksp](https://developer.android.com/build/migrate-to-ksp).

---

### [Dagger / Hilt](https://dagger.dev/hilt/) — Google

**What it does:** Compile-time dependency injection framework for Android. Hilt is the opinionated Android layer over Dagger. Supports KSP since Hilt 2.48, with current version at 2.57.1. KSP processing is up to 2x faster than kapt.

**Loop phase:** implement (DI wiring)

**Install (KSP):**
```kotlin
// build.gradle.kts
plugins {
    id("com.google.devtools.ksp")
    id("com.google.dagger.hilt.android") version "2.57.1"
}
dependencies {
    implementation("com.google.dagger:hilt-android:2.57.1")
    ksp("com.google.dagger:hilt-android-compiler:2.57.1")
    // AndroidX Hilt extensions (for WorkManager, etc.)
    ksp("androidx.hilt:hilt-compiler:1.2.0")
}
```

**Claude Code integration:** Hilt generates `_HiltComponents` and `_Factory` classes at compile time. When Claude Code adds `@Inject`, `@HiltViewModel`, or `@AndroidEntryPoint`, run `./gradlew build` to trigger code generation and verify wiring.

---

### [Room](https://developer.android.com/training/data-storage/room) — Google

**What it does:** SQLite abstraction layer for Android. Generates DAO implementations, migration helpers, and database classes at compile time. Room 3.0 (2026) is KSP-only, Kotlin-code-only, and coroutine-first — no more kapt or Java code generation. Supports Kotlin Multiplatform (Android, iOS, JVM).

**Loop phase:** implement (database layer code generation)

**Install (Room 3.0):**
```kotlin
// build.gradle.kts
plugins {
    id("com.google.devtools.ksp")
}
dependencies {
    implementation("androidx.room:room-runtime:3.0.0")
    implementation("androidx.room:room-ktx:3.0.0")
    ksp("androidx.room:room-compiler:3.0.0")
}
```

**Claude Code integration:** After writing `@Entity`, `@Dao`, and `@Database` classes, run `./gradlew kspDebugKotlin` to generate implementations. Schema export to JSON is useful for migration verification: `ksp { arg("room.schemaLocation", "$projectDir/schemas") }`.

---

## Build Tooling (implement/verify)

### Gradle CLI

**What it does:** The build system for virtually all Kotlin/Android projects. The Gradle wrapper (`./gradlew`) ensures reproducible builds with a pinned Gradle version.

**Key commands for Claude Code:**
```bash
# Build
./gradlew build                         # Full build (compile + test + lint)
./gradlew assembleDebug                 # Build debug APK/AAR
./gradlew assembleRelease               # Build release APK/AAR
./gradlew clean                         # Delete build directory

# Test
./gradlew test                          # Run all unit tests
./gradlew testDebugUnitTest             # Android debug unit tests
./gradlew connectedDebugAndroidTest     # Instrumented tests on device/emulator
./gradlew test --tests "*.MyTest"       # Run specific test class

# Lint & Analysis
./gradlew lint                          # Android Lint
./gradlew detekt                        # Detekt static analysis
./gradlew ktlintCheck                   # ktlint check
./gradlew ktlintFormat                  # ktlint auto-fix

# Dependencies
./gradlew dependencies                  # Full dependency tree
./gradlew :app:dependencies --configuration releaseRuntimeClasspath
./gradlew dependencyUpdates             # Check for newer versions (ben-manes plugin)

# Build Cache & Performance
./gradlew build --build-cache           # Enable build cache
./gradlew build --scan                  # Generate Develocity build scan
./gradlew build --profile              # Generate build performance report
./gradlew build --continue              # Don't stop on first failure
./gradlew build --rerun-tasks           # Ignore up-to-date checks
```

**Claude Code integration:** `./gradlew` is the primary shell-out target. Always use the wrapper, never bare `gradle`. Parse XML test reports at `build/test-results/` and lint reports at `build/reports/`.

---

### [Gradle Build Scans / Develocity](https://scans.gradle.com/)

**What it does:** Web-based build analysis. Captures dependency resolution, task execution times, test results, and failure details. Free public scans available at scans.gradle.com. Enterprise version (Develocity 2026.1) adds build caching and predictive test selection.

**Current version:** Develocity Gradle Plugin 4.4

**Loop phase:** verify (build performance analysis)

**Usage:**
```bash
./gradlew build --scan   # Generates a shareable build scan URL
```

**Claude Code integration:** Add `--scan` to any Gradle command to get a detailed analysis URL. Useful for diagnosing slow builds or flaky tests. The URL is printed to stdout at build completion.

---

### [Gradle Version Catalog](https://docs.gradle.org/current/userguide/version_catalogs.html) — Gradle

**What it does:** Centralizes dependency versions in a single `libs.versions.toml` file. Generates type-safe accessors for all modules. Sections: `[versions]`, `[libraries]`, `[bundles]`, `[plugins]`. Eliminates version duplication across multi-module projects.

**Loop phase:** implement (dependency declaration)

**File:** `gradle/libs.versions.toml`
```toml
[versions]
kotlin = "2.1.20"
hilt = "2.57.1"
room = "3.0.0"
coroutines = "1.10.2"

[libraries]
hilt-android = { module = "com.google.dagger:hilt-android", version.ref = "hilt" }
room-runtime = { module = "androidx.room:room-runtime", version.ref = "room" }
room-ktx = { module = "androidx.room:room-ktx", version.ref = "room" }
coroutines-test = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-test", version.ref = "coroutines" }

[bundles]
room = ["room-runtime", "room-ktx"]

[plugins]
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
ksp = { id = "com.google.devtools.ksp", version = "2.1.20-1.0.32" }
```

**Claude Code integration:** When adding dependencies, edit `gradle/libs.versions.toml` first, then reference via `libs.<alias>` in `build.gradle.kts`. Claude Code should always check the catalog before adding a dependency to avoid duplication.

---

### Gradle Convention Plugins

**What it does:** Encapsulates reusable build logic (Android config, Kotlin options, testing setup) in shared plugins within `buildSrc/` or `build-logic/`. Eliminates copy-paste across modules. Uses the version catalog for dependency references.

**Loop phase:** implement (build infrastructure)

**Structure:**
```
build-logic/
  convention/
    build.gradle.kts
    src/main/kotlin/
      AndroidApplicationConventionPlugin.kt
      AndroidLibraryConventionPlugin.kt
      KotlinAndroidConventionPlugin.kt
```

**Claude Code integration:** When Claude Code sees duplicated Gradle configuration across modules, convention plugins are the fix. Shell out to `./gradlew build` after modifying a convention plugin to verify all consuming modules still compile.

---

## Static Analysis (verify)

### [detekt](https://detekt.dev/) — Custom Rules

**What it does:** Beyond built-in rules, detekt supports custom rule sets for project-specific checks. Rules are Kotlin classes extending `Rule` with a `visitX()` pattern. Package as a JAR and add to detekt's classpath.

**Rule categories:** complexity, coroutines, empty-blocks, exceptions, naming, performance, potential-bugs, style

**Key config (detekt.yml):**
```yaml
complexity:
  LongMethod:
    maxLines: 60
  CyclomaticComplexMethod:
    threshold: 15
naming:
  FunctionNaming:
    functionPattern: '[a-z][a-zA-Z0-9]*'
```

**Claude Code integration:** Use `detekt --generate-config` to bootstrap, then tune thresholds. Claude Code can read detekt output and fix flagged issues in a verify-then-fix loop.

---

### [SonarQube / SonarCloud](https://www.sonarsource.com/knowledge/languages/kotlin/) — SonarSource

**What it does:** Continuous code quality platform with hundreds of Kotlin-specific rules. Supports symbolic execution, taint analysis, and security hotspot detection. Imports detekt findings. Available as SonarQube Server (self-hosted) or SonarCloud (hosted).

**Current version:** Kotlin analyzer 2.2+

**Loop phase:** verify (CI quality gate)

**Install:**
```kotlin
// build.gradle.kts
plugins {
    id("org.sonarqube") version "6.0.1.5171"
}
```

**Key commands:**
```bash
./gradlew sonar \
  -Dsonar.projectKey=my-project \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.token=$SONAR_TOKEN
```

**Claude Code integration:** Shell out to `./gradlew sonar` in CI. SonarQube's web API can be queried for issue details. Not typically run locally by Claude Code, but useful for understanding project-wide quality trends.

---

### [Semgrep](https://semgrep.dev/docs/languages/kotlin) — Semgrep Inc.

**What it does:** Lightweight static analysis with pattern-matching rules. Kotlin support is GA with framework-specific Pro rules. Covers 80% of critical CVEs since 2017 and 100% of critical+high CVEs since May 2022. Supply chain reachability analysis for Kotlin/Gradle (no lockfile required). December 2025 added new high-severity reachability rules for Java/Kotlin/Scala.

**Loop phase:** verify (security analysis)

**Install:**
```bash
pip install semgrep
# or
brew install semgrep
```

**Key commands:**
```bash
semgrep scan --config auto .                 # Auto-detect language, use recommended rules
semgrep scan --config p/kotlin .             # Kotlin-specific rules
semgrep scan --config p/owasp-top-ten .      # OWASP rules
semgrep ci                                   # CI mode with Semgrep Cloud findings
```

**Claude Code integration:** Shell out to `semgrep scan --config auto --json .` for structured output. Semgrep rules are YAML-based and easy to write custom patterns for project-specific checks. MCP integration available via the semgrep-plugin.

---

### [konsist](https://docs.konsist.lemonappdev.com/) — LemonAppDev

**What it does:** Architectural testing library for Kotlin (the ArchUnit equivalent). Write unit tests that enforce architectural boundaries, naming conventions, package structure, visibility modifiers, annotation placement, and layer dependencies. Supports hexagonal, onion, and 3-tier architectures. Works with JUnit and Kotest.

**Current version:** 0.17.3

**Loop phase:** verify (architectural conformance)

**Install:**
```kotlin
// build.gradle.kts
dependencies {
    testImplementation("com.lemonappdev:konsist:0.17.3")
}
```

**Usage example:**
```kotlin
@Test
fun `use cases should reside in domain layer`() {
    Konsist.scopeFromProject()
        .classes()
        .withNameEndingWith("UseCase")
        .assertTrue { it.resideInPackage("..domain..") }
}

@Test
fun `domain layer should not depend on data layer`() {
    Konsist.scopeFromProject()
        .assertArchitecture {
            val domain = Layer("Domain", "..domain..")
            val data = Layer("Data", "..data..")
            domain.doesNotDependOn(data)
        }
}
```

**Claude Code integration:** No CLI — runs as regular unit tests via `./gradlew test`. Claude Code can write konsist tests to enforce architectural decisions from the plan phase, then verify they pass.

---

## Dependency Management (implement)

### [Gradle Version Catalog](https://docs.gradle.org/current/userguide/version_catalogs.html)

See [Build Tooling > Gradle Version Catalog](#gradle-version-catalog---gradle) above.

---

### [Renovate](https://docs.renovatebot.com/modules/manager/gradle/) — Mend.io

**What it does:** Automated dependency update bot. Parses `build.gradle`, `build.gradle.kts`, `gradle.properties`, `libs.versions.toml`, and `versions.props`. Opens PRs with dependency bumps. Highly configurable (hundreds of options, config presets, grouping strategies). Supports Gradle wrapper updates.

**Loop phase:** implement (automated dependency freshness)

**Install:** GitHub App or self-hosted. Drops a `renovate.json` in repo root.

**Config example:**
```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "matchManagers": ["gradle"],
      "groupName": "Kotlin ecosystem",
      "matchPackagePatterns": ["^org.jetbrains.kotlin"]
    }
  ]
}
```

**Claude Code integration:** Not a direct Claude Code tool — runs as a GitHub bot. But Claude Code can review Renovate PRs, check changelogs, and verify builds after dependency bumps.

---

### [Dependabot](https://docs.github.com/en/code-security/dependabot) — GitHub

**What it does:** GitHub-native dependency update bot. Supports Gradle (build.gradle, build.gradle.kts, settings.gradle). Opens PRs for version bumps. Simpler configuration than Renovate but fewer customization options.

**Loop phase:** implement (automated dependency freshness)

**Config (`.github/dependabot.yml`):**
```yaml
version: 2
updates:
  - package-ecosystem: "gradle"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Claude Code integration:** Like Renovate — GitHub-native, not a CLI tool. Claude Code can review and test Dependabot PRs.

---

### [dependency-analysis-gradle-plugin](https://github.com/autonomousapps/dependency-analysis-gradle-plugin) — Tony Robalik

**What it does:** Finds unused dependencies, used-but-undeclared transitive dependencies, and misplaced dependencies (e.g., `implementation` vs `api` vs `debugImplementation`). Uses bytecode analysis. Variant-aware for Android projects. Detects unused annotation processors.

**Current version:** 3.5.1

**Loop phase:** verify (dependency hygiene)

**Install:**
```kotlin
// settings.gradle.kts
plugins {
    id("com.autonomousapps.dependency-analysis") version "3.5.1"
}
```

**Key commands:**
```bash
./gradlew buildHealth              # Aggregate advice across all modules
./gradlew :app:projectHealth       # Per-module advice
./gradlew :app:reason --id com.google.dagger:hilt-android  # Why is this dep needed?
```

**Claude Code integration:** Shell out to `./gradlew buildHealth`. Parse the console output or JSON at `build/reports/dependency-analysis/`. Use after adding/removing dependencies to verify correctness. The `reason` task is excellent for understanding transitive dependency chains.

---

## Documentation (implement)

### [Dokka](https://github.com/Kotlin/dokka) — JetBrains

**What it does:** Documentation engine for Kotlin. Understands KDoc comments and Java's Javadoc. Generates HTML (custom modern format), Javadoc HTML, GFM Markdown, and Jekyll Markdown. Supports mixed Kotlin/Java projects and Kotlin Multiplatform. K2 analysis is stable and default since Dokka 2.1.0.

**Current version:** 2.1.0 (2.2.0-Beta available)

**Loop phase:** implement (API documentation)

**Install:**
```kotlin
// build.gradle.kts
plugins {
    id("org.jetbrains.dokka") version "2.1.0"
}
```

**Key commands:**
```bash
./gradlew dokkaHtml                # Generate HTML docs
./gradlew dokkaGfm                 # Generate GitHub-flavored Markdown
./gradlew dokkaJavadoc             # Generate Javadoc-compatible output
./gradlew dokkaHtmlMultiModule     # Multi-module project docs
```

**Claude Code integration:** Shell out to `./gradlew dokkaHtml` to generate docs. Claude Code can write KDoc comments following the standard syntax, then verify they render correctly. Output goes to `build/dokka/`.

---

### KDoc Syntax Reference

**What it is:** Kotlin's documentation comment format (equivalent to Javadoc). Used by Dokka for generation.

**Key tags:**
```kotlin
/**
 * Brief summary of the function.
 *
 * Detailed description with [links to other symbols][OtherClass].
 *
 * @param name Description of parameter
 * @return Description of return value
 * @throws IllegalArgumentException when input is invalid
 * @sample com.example.samples.sampleFunction
 * @see OtherClass
 * @since 1.0.0
 * @suppress Hides from generated docs
 */
fun doSomething(name: String): Result { ... }
```

**Claude Code integration:** Claude Code should generate KDoc for all public API surfaces. The `@sample` tag references actual compilable code, which doubles as documentation and tests.

---

## Coroutine Tools (implement/verify)

### [kotlinx-coroutines-test](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/) — JetBrains

**What it does:** Official test utilities for Kotlin coroutines. `runTest` builder automatically skips `delay()` calls while preserving execution order. `TestDispatcher` types control virtual time. `StandardTestDispatcher` queues coroutines for manual advancement. `UnconfinedTestDispatcher` executes eagerly.

**Current version:** 1.10.2 (matches kotlinx.coroutines version)

**Loop phase:** verify (coroutine testing)

**Install:**
```kotlin
// build.gradle.kts
dependencies {
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.10.2")
}
```

**Key patterns:**
```kotlin
@Test
fun testCoroutine() = runTest {
    val result = myRepository.fetchData()  // delay() is auto-skipped
    assertEquals(expected, result)
}

@Test
fun testWithAdvancing() = runTest {
    val deferred = async { delay(1000); "result" }
    advanceTimeBy(1000)
    assertEquals("result", deferred.await())
}
```

**Claude Code integration:** Claude Code should wrap all coroutine tests in `runTest`. Use `advanceUntilIdle()` when testing code that launches child coroutines. Share the `testScheduler` across multiple `TestDispatcher` instances for consistent virtual time.

---

### [Turbine](https://github.com/cashapp/turbine) — Cash App

See [Testing Frameworks > Turbine](#turbinehttpsgithubcomcashappturbine--cash-app) above. Turbine is both a testing framework and a coroutine tool.

---

### Coroutine Debugging

**What it does:** Built-in debug tooling in kotlinx.coroutines. `DebugProbes` install coroutine tracking for stack trace enhancement and coroutine hierarchy dumps. JUnit 5 `CoroutinesTimeoutExtension` runs tests in a separate thread with timeout and auto-dumps coroutine state on failure.

**Enable debugging:**
```bash
# JVM system property
-Dkotlinx.coroutines.debug
```

```kotlin
// Programmatic installation
DebugProbes.install()
DebugProbes.dumpCoroutines()
```

**JUnit 5 extension:**
```kotlin
// build.gradle.kts
dependencies {
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-debug:1.10.2")
}
```

**Claude Code integration:** When debugging hanging tests, add `-Dkotlinx.coroutines.debug` to the Gradle test JVM args. The `DebugProbes.dumpCoroutines()` output shows all active coroutines with their creation stack traces — useful for diagnosing deadlocks.

---

## Dependency Security (verify)

### [Snyk](https://snyk.io/) — Snyk

**What it does:** SCA (Software Composition Analysis) tool that scans Gradle dependencies for known vulnerabilities. Supports both Groovy and Kotlin DSL build files. Gradle plugin (0.7.0) runs as a build task. Snyk CLI provides richer output and monitoring capabilities.

**Current version:** Gradle plugin 0.7.0; Snyk CLI updated continuously

**Loop phase:** verify (vulnerability scanning)

**Install:**
```kotlin
// build.gradle.kts — Gradle plugin
plugins {
    id("io.snyk.gradle.plugin.snykplugin") version "0.7.0"
}
```
```bash
# CLI (preferred)
brew install snyk
snyk auth   # One-time authentication
```

**Key commands:**
```bash
snyk test --gradle-sub-project=app    # Test specific module
snyk test --all-sub-projects          # Test all modules
snyk monitor                          # Upload to Snyk dashboard for monitoring
snyk test --severity-threshold=high   # Only fail on high/critical
```

**Claude Code integration:** Shell out to `snyk test` for on-demand scanning. Parse JSON output (`snyk test --json`). Use `--severity-threshold` to control noise level. Snyk CLI is more flexible than the Gradle plugin.

---

### [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/) — OWASP Foundation

**What it does:** SCA tool that identifies known vulnerable dependencies by matching them against the NVD (National Vulnerability Database). Gradle plugin generates HTML/JSON/XML reports. Supports Java, Kotlin, and other JVM dependencies.

**Current version:** 12.2.0 (January 2026)

**Loop phase:** verify (CVE scanning)

**Install:**
```kotlin
// build.gradle.kts
plugins {
    id("org.owasp.dependencycheck") version "12.2.0"
}
```

**Key commands:**
```bash
./gradlew dependencyCheckAnalyze   # Run analysis
./gradlew dependencyCheckPurge     # Clear local NVD cache
```

**Configuration:**
```kotlin
dependencyCheck {
    failBuildOnCVSS = 7.0f          // Fail on High+ CVEs
    formats = listOf("HTML", "JSON")
    suppressionFile = "owasp-suppressions.xml"
}
```

**Note:** Since September 2025, Sonatype OSSIndex requires API tokens. Configure username/password if using OSSIndex as a data source.

**Claude Code integration:** Shell out to `./gradlew dependencyCheckAnalyze`. Parse the HTML report at `build/reports/dependency-check-report.html`. Use suppression files for false positives. Slower than Snyk (downloads NVD data) but fully open-source.

---

### [Socket.dev](https://socket.dev/) — Socket

**What it does:** Supply chain security platform that inspects packages for risky behaviors (network calls, obfuscated code, unsafe filesystem operations) rather than just matching CVEs. Kotlin/Gradle support added in 2025. Analyzes `build.gradle`, `build.gradle.kts`, and `gradle.lockfile`. Generates SBOM via CycloneDX.

**Loop phase:** verify (supply chain risk analysis)

**Install:**
```bash
npm install -g @socketsecurity/cli
# or integrate via GitHub App
```

**Usage:**
```bash
socket scan create --repo . --branch main   # Scan current project
```

**Claude Code integration:** Socket is primarily a GitHub integration / CI tool. The CLI can be used for local scanning. Complements CVE-based tools (Snyk, OWASP) by detecting malicious behavior patterns that don't have CVE entries yet.

---

## Tool Selection Quick Reference

| Need | Recommended Tool | Runner |
|------|-----------------|--------|
| Format Kotlin code | ktlint or ktfmt (pick one) | `./gradlew ktlintFormat` or `ktfmt` |
| Static analysis | detekt | `./gradlew detekt` |
| Android-specific lint | Android Lint | `./gradlew lint` |
| Unit tests | JUnit 5 + MockK | `./gradlew test` |
| Property testing | Kotest | `./gradlew test` |
| Flow testing | Turbine | `./gradlew test` |
| Coroutine testing | kotlinx-coroutines-test | `./gradlew test` |
| Android unit tests (no emulator) | Robolectric | `./gradlew testDebugUnitTest` |
| Annotation processing | KSP (not kapt) | `./gradlew build` |
| Dependency injection | Hilt + KSP | `./gradlew build` |
| Architectural testing | konsist | `./gradlew test` |
| Unused dependencies | dependency-analysis-gradle-plugin | `./gradlew buildHealth` |
| Dependency versions | Gradle Version Catalog | Edit `libs.versions.toml` |
| Automated updates | Renovate or Dependabot | GitHub bot |
| API docs | Dokka | `./gradlew dokkaHtml` |
| Security scanning | Snyk CLI or OWASP dependency-check | `snyk test` or `./gradlew dependencyCheckAnalyze` |
| SAST | Semgrep | `semgrep scan --config auto` |
| Supply chain | Socket.dev | GitHub integration |

---

## Sources

- [ktlint — Pinterest](https://github.com/pinterest/ktlint)
- [ktlint 1.8.0 Features](https://pinterest.github.io/ktlint/1.8.0/)
- [detekt — Static Analysis for Kotlin](https://detekt.dev/)
- [detekt — GitHub](https://github.com/detekt/detekt)
- [ktfmt — Meta](https://facebook.github.io/ktfmt/)
- [ktfmt — GitHub](https://github.com/facebook/ktfmt)
- [Adopting Ktfmt and Detekt — Block Engineering](https://engineering.block.xyz/blog/adopting-ktfmt-and-detekt)
- [diktat — SaveOurTool](https://diktat.saveourtool.com/)
- [Android Lint — Android Developers](https://developer.android.com/studio/write/lint)
- [Android Custom Lint Rules](https://googlesamples.github.io/android-custom-lint-rules/)
- [Kotest](https://kotest.io/)
- [Kotest Property Testing](https://kotest.io/docs/proptest/property-based-testing.html)
- [MockK](https://mockk.io/)
- [MockK — GitHub](https://github.com/mockk/mockk)
- [Turbine — Cash App](https://github.com/cashapp/turbine)
- [kotlin-test — Kotlin Documentation](https://kotlinlang.org/api/kotlin-test/)
- [Robolectric](https://robolectric.org/)
- [KSP — Google](https://github.com/google/ksp)
- [KSP Overview — Kotlin Documentation](https://kotlinlang.org/docs/ksp-overview.html)
- [Migrate from kapt to KSP — Android Developers](https://developer.android.com/build/migrate-to-ksp)
- [Dagger Hilt — Google](https://dagger.dev/hilt/)
- [Dagger KSP Guide](https://dagger.dev/dev-guide/ksp.html)
- [Room 3.0 — Android Developers Blog](https://android-developers.googleblog.com/2026/03/room-30-modernizing-room.html)
- [Room — Android Developers](https://developer.android.com/training/data-storage/room)
- [Gradle CLI Reference](https://docs.gradle.org/current/userguide/command_line_interface.html)
- [Gradle Version Catalogs](https://docs.gradle.org/current/userguide/version_catalogs.html)
- [Gradle Best Practices — Kotlin Documentation](https://kotlinlang.org/docs/gradle-best-practices.html)
- [Develocity Build Scan](https://gradle.com/develocity/product/build-scan/)
- [konsist — LemonAppDev](https://docs.konsist.lemonappdev.com/)
- [konsist — GitHub](https://github.com/LemonAppDev/konsist)
- [SonarQube Kotlin — SonarSource](https://www.sonarsource.com/knowledge/languages/kotlin/)
- [Semgrep Kotlin Support](https://semgrep.dev/docs/languages/kotlin)
- [Semgrep Kotlin Reachability](https://semgrep.dev/blog/2024/announcing-kotlin-reachability/)
- [dependency-analysis-gradle-plugin — GitHub](https://github.com/autonomousapps/dependency-analysis-gradle-plugin)
- [Renovate Gradle Manager](https://docs.renovatebot.com/modules/manager/gradle/)
- [Dokka — JetBrains](https://github.com/Kotlin/dokka)
- [KDoc — Kotlin Documentation](https://kotlinlang.org/docs/kotlin-doc.html)
- [kotlinx-coroutines-test — Kotlin Documentation](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/)
- [Testing Coroutines — Android Developers](https://developer.android.com/kotlin/coroutines/test)
- [Snyk CLI for Java and Kotlin](https://docs.snyk.io/supported-languages/supported-languages-list/java-and-kotlin/snyk-cli-for-java-and-kotlin)
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [OWASP Dependency-Check Gradle Plugin](https://plugins.gradle.org/plugin/org.owasp.dependencycheck)
- [Socket.dev Gradle Setup](https://docs.socket.dev/docs/gradle-setup-instructions-for-java-kotlin-and-scala)
- [JUnit 5 for Kotlin — Baeldung](https://www.baeldung.com/kotlin/junit-5-kotlin)
- [Kotlin Multiplatform Testing Guide 2025](https://www.kmpship.app/blog/kotlin-multiplatform-testing-guide-2025)

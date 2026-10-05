---
id: ef81bdb5-e189-44ed-be6e-867bff16f45b
title: Android UI Verification Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/android/ui-verification
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Android UI Verification Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Android UI Verification Tools

**Date:** 2026-03-29
**Context:** UI verification and visual testing tools for Android development (Jetpack Compose and View system), integrated with Claude Code workflows.

---

## Compose Screenshot Testing (verify)

### Paparazzi

- **Link:** [github.com/cashapp/paparazzi](https://github.com/cashapp/paparazzi)
- **Description:** JVM-only screenshot testing library by Cash App. Renders Android screens using LayoutLib (the same renderer Android Studio uses for previews) without a physical device or emulator. Supports both Composables and Android Views. Almost twice as fast as Google's Compose Preview Screenshot Testing because it runs entirely on the JVM. Current version: 2.0.0-alpha04. Requires Java 17+.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts (module)
  plugins {
      id("app.cash.paparazzi") version "2.0.0-alpha04"
  }
  ```
  ```kotlin
  // Record baselines:   ./gradlew :module:recordPaparazziDebug
  // Verify screenshots: ./gradlew :module:verifyPaparazziDebug
  ```
  ```kotlin
  // Test class (src/test/)
  class MyScreenTest {
      @get:Rule val paparazzi = Paparazzi()

      @Test fun default() {
          paparazzi.snapshot { MyComposable() }
      }
  }
  ```
- **How Claude Code can use it:** Run `./gradlew :module:verifyPaparazziDebug` after UI changes to detect visual regressions. On failure, inspect the diff images in `build/reports/paparazzi/` to identify what changed. Record new baselines with `recordPaparazziDebug` when changes are intentional.
- **Limitations:** Composables must live in `com.android.library` modules (not `com.android.application`) due to resource bytecode format. No device-specific rendering (system bars, fonts). No interaction testing — snapshots only.

### Compose Preview Screenshot Testing (Google)

- **Link:** [developer.android.com/studio/preview/compose-screenshot-testing](https://developer.android.com/studio/preview/compose-screenshot-testing)
- **Description:** Google's official screenshot testing tool, announced at Google I/O 2024. Leverages existing `@Preview` annotated composables as test inputs. Runs on the host JVM using LayoutLib. Minimal setup — if you already have `@Preview` functions, those become your screenshot tests automatically. Still experimental (version 0.0.1-alpha08+).
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts (module)
  plugins {
      id("com.android.compose.screenshot") version "0.0.1-alpha08"
  }
  ```
  ```kotlin
  // Record:  ./gradlew updateDebugScreenshotTest
  // Verify:  ./gradlew validateDebugScreenshotTest
  ```
  Previews are automatically discovered — no test class needed. Any `@Preview` composable in the `screenshotTest` source set becomes a test.
- **How Claude Code can use it:** After modifying composables, run `validateDebugScreenshotTest` to check for regressions. This is the lowest-friction option if the project already uses `@Preview` annotations extensively. Failed tests produce diff images.
- **Limitations:** Early alpha — API may change. Slower than Paparazzi. Limited configuration options compared to Paparazzi or Roborazzi.

### Roborazzi

- **Link:** [github.com/takahirom/roborazzi](https://github.com/takahirom/roborazzi)
- **Description:** JVM screenshot testing built on Robolectric. The most feature-rich option — supports Activity, Fragment, Composable, and interaction-based screenshots (click, scroll, then capture). Integrates with Hilt for dependency injection in tests. Supports time-based captures for animated components via `@RoboComposePreviewOptions`. Auto-generates tests from Compose Previews via ComposablePreviewScanner integration.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts (module)
  plugins {
      id("io.github.takahirom.roborazzi") version "<latest>"
  }
  testImplementation("io.github.takahirom.roborazzi:roborazzi:<latest>")
  testImplementation("io.github.takahirom.roborazzi:roborazzi-compose:<latest>")
  ```
  ```kotlin
  // Record:  ./gradlew recordRoborazziDebug
  // Verify:  ./gradlew verifyRoborazziDebug
  // Compare: ./gradlew compareRoborazziDebug
  ```
- **How Claude Code can use it:** Run `verifyRoborazziDebug` to check regressions. Roborazzi can capture screenshots after interactions (simulating user flows), making it useful for verifying state transitions. The `compareRoborazziDebug` task generates side-by-side diff reports.
- **Limitations:** Depends on Robolectric, which adds test startup time. Rendering fidelity depends on Robolectric's Android simulation.

### Showkase

- **Link:** [github.com/airbnb/Showkase](https://github.com/airbnb/Showkase)
- **Description:** Annotation-processor library by Airbnb that creates a component browser app from `@Preview`, `@ShowkaseComposable`, `@ShowkaseColor`, and `@ShowkaseTypography` annotations. Provides a visual catalog of all composables, colors, and typography in a developer build. Integrates with Paparazzi for automatic screenshot testing of every cataloged component. Shows composables in multiple states (dark mode, larger fonts, RTL).
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  implementation("com.airbnb.android:showkase:1.0.3")
  ksp("com.airbnb.android:showkase-processor:1.0.3")
  // For screenshot testing:
  testImplementation("com.airbnb.android:showkase-screenshot-testing-paparazzi:1.0.3")
  ```
- **How Claude Code can use it:** Use Showkase as a visual inventory of all UI components. Combine with Paparazzi to automatically screenshot-test every component in the catalog. When adding new composables, annotate with `@ShowkaseComposable` to include them in the test suite.
- **Limitations:** Requires annotation processing (KSP). Adds build time. Component browser is only useful in debug builds.

### ComposablePreviewScanner

- **Link:** [github.com/sergio-sastre/ComposablePreviewScanner](https://github.com/sergio-sastre/ComposablePreviewScanner)
- **Description:** Meta-library that scans all `@Preview` composables in your project and feeds them to any screenshot testing library — JVM-based (Paparazzi, Roborazzi) or instrumentation-based (Shot, Dropshots, Android-Testify). Supports `@PreviewParameter`, multi-previews (`@PreviewScreenSizes`, `@PreviewFontScales`, `@PreviewLightDark`, `@PreviewDynamicColors`), and custom multi-previews. Over 150k monthly downloads.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // For JVM tests (Paparazzi/Roborazzi):
  testImplementation("io.github.sergio-sastre.ComposablePreviewScanner:jvm:<latest>")
  // For instrumentation tests (Shot/Dropshots/Testify):
  androidTestImplementation("io.github.sergio-sastre.ComposablePreviewScanner:android:<latest>")
  ```
- **How Claude Code can use it:** Auto-generate screenshot tests from existing `@Preview` functions without writing individual test cases. Pair with Paparazzi or Roborazzi for zero-boilerplate screenshot coverage of all previews.

---

## View System Screenshot Testing (verify)

### Shot

- **Link:** [github.com/pedrovgs/Shot](https://github.com/pedrovgs/Shot)
- **Description:** Gradle plugin by Karumi built on Facebook's Screenshot Tests SDK. Instrumentation-based — runs on a device or emulator. Automatically disables flaky components (cursors, scrollbars, animations) before capture. Supports both Android Views and Compose.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  plugins {
      id("com.karumi.shot") version "<latest>"
  }
  android {
      defaultConfig {
          testInstrumentationRunner = "com.karumi.shot.ShotTestRunner"
      }
  }
  ```
  ```bash
  # Record baselines:
  ./gradlew executeScreenshotTests -Precord
  # Verify:
  ./gradlew executeScreenshotTests
  ```
- **How Claude Code can use it:** Run `./gradlew executeScreenshotTests` after View-based UI changes. Shot handles animation/cursor disabling automatically, reducing flakiness. Requires a running emulator.
- **Limitations:** Requires device/emulator. Slower than JVM-based alternatives. Based on Facebook's SDK which has limited maintenance.

### Dropshots

- **Link:** [github.com/dropbox/dropshots](https://github.com/dropbox/dropshots)
- **Description:** On-device screenshot testing by Dropbox. Unique approach: pushes reference images to the device and performs comparison on-device, making it suitable for validating system integrations like edge-to-edge display on Android 15. Includes `CountValidator` (max pixel differences) and `ThresholdValidator` (percentage tolerance).
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  plugins {
      id("com.dropbox.dropshots") version "0.5.1"
  }
  ```
  ```kotlin
  // Test class
  class MyViewTest {
      @get:Rule val dropshots = Dropshots()

      @Test fun myView() {
          // Setup view...
          dropshots.assertSnapshot(view)
      }
  }
  ```
  ```bash
  # Record:  ./gradlew connectedAndroidTest -Pdropshots.record
  # Verify:  ./gradlew connectedAndroidTest
  ```
- **How Claude Code can use it:** Ideal for testing device-specific rendering (edge-to-edge, system bars, Material You dynamic colors). Run instrumentation tests after changes that affect system integration. Configure tolerance thresholds to avoid false positives from anti-aliasing.
- **Limitations:** Requires device/emulator. Reference images are device-resolution-specific.

### Android-Testify

- **Link:** [github.com/ndtp/android-testify](https://github.com/ndtp/android-testify)
- **Description:** Originally by Shopify, now community-maintained. Testify 2.0 separates core screenshot functionality from JUnit4 lifecycle, supporting classic Views, Compose UI, and Surface Views. Includes Gradle plugin for recording/verifying and an IntelliJ/Android Studio plugin for GUI access. Natively supports grouping tests by device characteristics (resolution, orientation, API level, language).
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  plugins {
      id("dev.testify") version "<latest>"
  }
  androidTestImplementation("dev.testify:testify:<latest>")
  ```
  ```bash
  # Record:  ./gradlew screenshotRecord
  # Verify:  ./gradlew screenshotTest
  ```
- **How Claude Code can use it:** Good for projects with mixed View/Compose UI. The device-characteristics grouping helps when testing across multiple configurations. Android Studio plugin provides quick access to recording and verification.

---

## UI Testing Frameworks (verify)

### Compose UI Test

- **Link:** [developer.android.com/develop/ui/compose/testing](https://developer.android.com/develop/ui/compose/testing)
- **Description:** Official testing framework for Jetpack Compose. Uses the semantics tree (not the rendered UI) for finding and asserting on nodes. Provides `ComposeTestRule` for setting content and `ComposeContentTestRule` for instrumentation. Finders: `onNodeWithText()`, `onNodeWithContentDescription()`, `onNodeWithTag()`, `onAllNodesWithText()`. Actions: `performClick()`, `performScrollTo()`, `performTextInput()`. Assertions: `assertIsDisplayed()`, `assertExists()`, `assertTextEquals()`, `assertIsEnabled()`.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  androidTestImplementation("androidx.compose.ui:ui-test-junit4:<compose-version>")
  debugImplementation("androidx.compose.ui:ui-test-manifest:<compose-version>")
  ```
  ```kotlin
  @get:Rule val rule = createComposeRule()

  @Test fun greeting_displayed() {
      rule.setContent { GreetingScreen("World") }
      rule.onNodeWithText("Hello, World!").assertIsDisplayed()
  }
  ```
- **How Claude Code can use it:** Write and run Compose UI tests to verify behavioral correctness after changes. Tests operate on the semantics tree, making them resilient to visual changes that don't affect functionality. Run with `./gradlew connectedAndroidTest` or specific test classes.

### Espresso

- **Link:** [developer.android.com/training/testing/espresso](https://developer.android.com/training/testing/espresso/basics)
- **Description:** Google's UI testing framework for Android Views (2013+). Three core components: `ViewMatchers` (find views: `withId()`, `withText()`, `withTagKey()`), `ViewActions` (perform actions: `click()`, `longClick()`, `scrollTo()`, `typeText()`), `ViewAssertions` (verify state: `matches()`, `doesNotExist()`). Synchronizes automatically with the UI thread — waits for idle before assertions.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  androidTestImplementation("androidx.test.espresso:espresso-core:3.6.1")
  androidTestImplementation("androidx.test:runner:1.6.2")
  ```
  ```kotlin
  @Test fun buttonClick_showsResult() {
      onView(withId(R.id.my_button)).perform(click())
      onView(withId(R.id.result_text)).check(matches(withText("Clicked")))
  }
  ```
- **How Claude Code can use it:** Run Espresso tests after View-based UI changes. Espresso's automatic synchronization reduces flakiness. For projects migrating from Views to Compose, Espresso and Compose UI Test can coexist in the same test suite.

### UI Automator

- **Link:** [developer.android.com/training/testing/other-components/ui-automator](https://developer.android.com/training/testing/other-components/ui-automator)
- **Description:** Cross-app UI testing framework. Unlike Espresso (single-app), UI Automator can interact with any app on the device including system settings, permission dialogs, notifications, and quick settings. Version 2.4 introduces a Kotlin-friendly DSL with predicate-based element finding. Essential for testing system integration points.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  androidTestImplementation("androidx.test.uiautomator:uiautomator:2.4.0")
  ```
  ```kotlin
  val device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())
  device.findObject(By.text("Allow")).click()
  ```
- **How Claude Code can use it:** Use for testing flows that cross app boundaries — permission dialogs, share intents, notification handling, deep links from other apps. Combine with Espresso/Compose UI Test for end-to-end flows that start in your app, leave it, and return.

---

## Accessibility Testing (verify)

### Accessibility Test Framework (ATF)

- **Link:** [developer.android.com/training/testing/espresso/accessibility-checking](https://developer.android.com/training/testing/espresso/accessibility-checking)
- **Description:** Google's open-source library that integrates with Espresso to automatically detect accessibility issues during UI testing. Runs checks whenever a `ViewAction` is performed — examines the view and surrounding UI for accessibility violations. Reports issues as ERROR, WARNING, or INFO. One line of code enables it for all existing Espresso tests.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  androidTestImplementation("androidx.test.espresso:espresso-accessibility:3.6.1")
  ```
  ```kotlin
  // Enable in test setup (one line):
  @Before fun setUp() {
      AccessibilityChecks.enable()
  }
  ```
- **How Claude Code can use it:** Add `AccessibilityChecks.enable()` to test setup. All existing Espresso tests will automatically check for accessibility issues — no test rewrites needed. Review ERROR-level findings as mandatory fixes.

### Accessibility Scanner

- **Link:** [Google Play: Accessibility Scanner](https://play.google.com/store/apps/details?id=com.google.android.apps.accessibility.auditor)
- **Description:** Standalone Android app by Google that scans any app's UI for accessibility improvements. Uses ATF under the hood. Does not require source code access — works on any installed app. Highlights issues like missing content descriptions, small touch targets, and low contrast.
- **Loop phase:** verify
- **Install/usage:** Install from Google Play. Enable in Settings > Accessibility. Tap the floating button on any screen to scan.
- **How Claude Code can use it:** Claude Code cannot directly invoke Accessibility Scanner (it's a GUI app). However, after deploying a debug build to a device, a developer can run the scanner and share results. For automated CI, use ATF/Espresso integration instead.

### Compose Semantics Testing

- **Link:** [developer.android.com/develop/ui/compose/testing/semantics](https://developer.android.com/develop/ui/compose/testing/semantics)
- **Description:** Compose UI tests operate on the semantics tree, which is the same tree used by accessibility services (TalkBack, Switch Access). This means every Compose UI test is implicitly an accessibility test — if a node cannot be found via semantics, it is also invisible to accessibility services. Key properties: `contentDescription` (screen reader labels), `testTag` (test identifiers), `role`, `stateDescription`.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // Composable with proper semantics:
  IconButton(
      onClick = { /* ... */ },
      modifier = Modifier.semantics { contentDescription = "Add to favorites" }
  ) { Icon(Icons.Default.Favorite, contentDescription = null) }

  // Test verifying accessibility:
  rule.onNodeWithContentDescription("Add to favorites").assertIsDisplayed()
  ```
- **How Claude Code can use it:** When writing Compose UI tests, prefer `onNodeWithContentDescription()` over `onNodeWithTag()` where possible — this simultaneously verifies that accessibility labels exist and are correct. If a composable cannot be found by content description, it likely has an accessibility gap.
- **Best practice:** Do not use `contentDescription` on purely decorative images — set it to `null`. Use `testTag` only when semantic properties are insufficient for test identification.

---

## Visual Regression (verify)

### Screenshotbot

- **Link:** [screenshotbot.io](https://screenshotbot.io/) | [github.com/screenshotbot/screenshotbot-oss](https://github.com/screenshotbot/screenshotbot-oss)
- **Description:** CI-integrated screenshot testing platform. Provides a Gradle plugin that auto-detects your screenshot library (Paparazzi, Shot, screenshot-tests-for-android) and uploads screenshots after each CI run. Tracks screenshots per commit across branches — automatically determines the baseline commit for comparison rather than requiring manual golden-image approval. Provides PR notifications when screenshots change. Eliminates the need for Git LFS to store baseline images. Open-source self-hosted option available.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  plugins {
      id("io.screenshotbot") version "<latest>"
  }
  ```
  In CI, the Screenshotbot CLI uploads screenshots after test execution and posts status checks to GitHub/GitLab PRs.
- **How Claude Code can use it:** After running screenshot tests locally, review Screenshotbot's web dashboard for visual diffs. In CI pipelines, Screenshotbot blocks PR merges when unreviewed visual changes are detected.

### Applitools Eyes

- **Link:** [applitools.com](https://applitools.com/)
- **Description:** Commercial AI-powered visual testing platform. Uses Visual AI (not pixel-by-pixel comparison) to detect meaningful layout and visual changes while ignoring rendering noise. Integrates with Espresso, Appium, and other Android testing frameworks. Cross-platform — can compare Android, iOS, and web screenshots of the same feature.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  androidTestImplementation("com.applitools:eyes-android-espresso:5.x.x")
  ```
  ```kotlin
  val eyes = Eyes()
  eyes.open(activity, "App", "Test")
  eyes.checkWindow("Main Screen")
  eyes.close()
  ```
- **How Claude Code can use it:** Applitools provides an SDK and CLI. After running tests, the Applitools dashboard shows AI-analyzed diffs. Useful for large teams where pixel-level comparison produces too many false positives.
- **Limitations:** Commercial product with usage-based pricing. Requires network access for AI comparison.

### Visual Regression Tracker (self-hosted)

- **Link:** [github.com/Visual-Regression-Tracker](https://github.com/Visual-Regression-Tracker/Visual-Regression-Tracker)
- **Description:** Open-source, self-hosted visual regression platform. Platform-agnostic — integrates with any test runner that can capture screenshots. Provides baseline management, region ignoring, and history tracking. Docker-based deployment.
- **Loop phase:** verify
- **Install/usage:** Deploy via Docker Compose. Upload screenshots from tests via REST API or language-specific SDKs. Review diffs in the web dashboard.
- **How Claude Code can use it:** Self-hosted alternative to Screenshotbot/Applitools for teams that need to keep screenshots on-premises. Claude Code can trigger screenshot uploads via CLI after test runs.

---

## Screenshot Capture & Comparison (verify)

### adb screencap

- **Link:** [developer.android.com/tools/adb](https://developer.android.com/tools/adb)
- **Description:** Built-in ADB command for capturing device/emulator screenshots. Captures exactly what the user sees, including system UI, status bar, and navigation bar. Fastest way to capture a full-screen screenshot.
- **Loop phase:** verify
- **Install/usage:**
  ```bash
  # Capture screenshot on device:
  adb shell screencap /sdcard/screenshot.png
  # Pull to local machine:
  adb pull /sdcard/screenshot.png ./screenshot.png
  ```
- **How Claude Code can use it:** After deploying a debug build, use `adb shell screencap` to capture the current screen state. Compare before/after screenshots manually or with a bitmap comparison library. Useful for quick ad-hoc verification without setting up a testing framework.

### UiDevice.takeScreenshot()

- **Link:** [developer.android.com/reference/androidx/test/uiautomator/UiDevice](https://developer.android.com/reference/androidx/test/uiautomator/UiDevice)
- **Description:** Programmatic screenshot capture within instrumentation tests. Captures the full device screen including system UI. Can be called at any point during a UI Automator or Espresso test.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  val device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())
  device.takeScreenshot(File("/sdcard/test_screenshot.png"))
  ```
- **How Claude Code can use it:** Embed in instrumentation tests to capture screenshots at specific test checkpoints. Combine with a comparison library for custom assertion logic.

### Compose captureToImage()

- **Link:** [developer.android.com/develop/ui/compose/testing](https://developer.android.com/develop/ui/compose/testing)
- **Description:** Compose testing API that captures a specific composable node as an `ImageBitmap`. Unlike full-screen captures, this isolates the exact component under test. Available on `SemanticsNodeInteraction` via the `captureToImage()` extension.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  val bitmap = rule.onNodeWithTag("my_card").captureToImage()
  // Compare bitmap.toPixelMap() with reference image
  ```
- **How Claude Code can use it:** Use `captureToImage()` in Compose UI tests to capture individual components for comparison. This is the foundation that screenshot testing libraries like Paparazzi and Roborazzi build upon. For custom comparisons, convert to a `Bitmap` and use pixel comparison.

### Bitmap Comparison Approaches

- **Description:** Android screenshot testing fundamentally works by comparing `Bitmap` objects pixel-by-pixel. Most libraries use this internally but you can also build custom comparisons.
- **Loop phase:** verify
- **Key patterns:**
  - **Pixel-exact comparison:** Compare every pixel — strict but prone to false positives from anti-aliasing, font rendering, and GPU differences.
  - **Threshold comparison:** Allow a percentage of pixels to differ (Dropshots' `ThresholdValidator`, custom tolerance settings).
  - **Perceptual comparison:** Compare perceived visual similarity rather than exact pixels — more robust but requires specialized libraries.
  - **Region masking:** Exclude dynamic content areas (timestamps, ads, avatars) from comparison.
- **How Claude Code can use it:** When a screenshot test fails, check whether the failure is a true regression or a rendering artifact. Configure appropriate tolerance thresholds in the project's screenshot testing library to reduce false positives without hiding real issues.

---

## Design Verification (verify)

### Material Design Compliance

- **Link:** [m3.material.io](https://m3.material.io/) | [Figma: Material 3 & Android 15](https://www.figma.com/community/file/809865700885504168/material-3-android-15)
- **Description:** Material 3 provides official Figma design kits with 1000+ components. Use these as the source of truth for verifying Compose Material3 implementations. The Figma kit includes component specs, spacing, typography scales, and color system definitions.
- **Loop phase:** verify
- **How Claude Code can use it:** When implementing Material3 components, cross-reference the Figma kit specs for correct spacing, elevation, and color token usage. Write Compose UI tests that assert on specific padding, text style, and color values to enforce Material compliance programmatically.

### Relay (Sunset April 2025)

- **Link:** [relay.material.io](https://relay.material.io/)
- **Description:** Google's Figma-to-Compose code generation tool. Imported Figma component metadata and generated pixel-perfect Compose code. **Sunset on April 30, 2025.** No longer available for new projects.
- **Loop phase:** N/A (discontinued)
- **Alternatives after sunset:**
  - **Manual conversion** — remains the most reliable method for complex screens.
  - **AI-assisted conversion** — use Claude Code, Gemini, or Copilot to translate Figma specs into Compose code. Provide the design spec (dimensions, colors, typography) and have Claude generate the composable.
  - **Design System Compliance Checker** (Figma plugin) — audits Figma files for consistency with design system tokens.
- **How Claude Code can use it:** With Relay gone, Claude Code's role in design verification increases. Given design specs (screenshots, Figma exports, or written requirements), Claude can generate Compose code and verify it against the specs. Use screenshot testing to capture the result and compare against design mockups.

### Figma Design System Compliance Checker

- **Link:** [Figma Community Plugin](https://www.figma.com/community/plugin/1577978298506710437/design-system-compliance-checker)
- **Description:** Figma plugin that audits design files for consistency with design system variables. Checks that designs use proper tokens (colors, spacing, typography) rather than hardcoded values. Works with Figma's variables system.
- **Loop phase:** verify
- **How Claude Code can use it:** While the plugin runs in Figma (not accessible to Claude Code directly), the audit results can be exported and used to verify that the Compose implementation uses the correct design tokens. Claude Code can grep the codebase for hardcoded color values, spacing values, or font sizes that should use theme tokens instead.

---

## Performance UI Testing (verify)

### Macrobenchmark

- **Link:** [developer.android.com/topic/performance/benchmarking/macrobenchmark-overview](https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview)
- **Description:** Measures end-user-visible performance: app startup (cold/warm/hot), scroll smoothness, animation frame times, and power consumption. Runs on real devices via instrumentation. Metrics: `StartupTimingMetric`, `FrameTimingMetric`, `TraceSectionMetric`, `PowerMetric`. Can generate and validate Baseline Profiles. Version 3 (2025) includes AI-based Baseline Profile hints, improved Compose LazyColumn/LazyGrid benchmarking, and automatic startup mode detection.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // Separate benchmark module (com.android.test)
  // build.gradle.kts
  plugins {
      id("com.android.test")
  }
  dependencies {
      implementation("androidx.benchmark:benchmark-macro-junit4:1.3.3")
  }
  ```
  ```kotlin
  @RunWith(AndroidJUnit4::class)
  class StartupBenchmark {
      @get:Rule
      val benchmarkRule = MacrobenchmarkRule()

      @Test
      fun startup() = benchmarkRule.measureRepeated(
          packageName = "com.example.app",
          metrics = listOf(StartupTimingMetric()),
          iterations = 5,
          startupMode = StartupMode.COLD
      ) {
          pressHome()
          startActivityAndWait()
      }
  }
  ```
  ```bash
  ./gradlew :benchmark:connectedBenchmarkAndroidTest
  ```
- **How Claude Code can use it:** Run Macrobenchmarks before and after performance-sensitive changes (startup optimizations, lazy list implementations, animation changes). Compare `FrameTimingMetric` results to detect jank regressions. Use `StartupTimingMetric` to verify that startup time stays within budget.

### Microbenchmark

- **Link:** [developer.android.com/topic/performance/benchmarking/microbenchmark-overview](https://developer.android.com/topic/performance/benchmarking/microbenchmark-overview)
- **Description:** Measures isolated code blocks — individual functions, algorithms, data transformations. Runs in a tight loop with JIT warmup to produce stable, repeatable measurements. Useful for verifying that a specific computation (layout calculation, data parsing, image processing) meets performance requirements.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  androidTestImplementation("androidx.benchmark:benchmark-junit4:1.3.3")
  ```
  ```kotlin
  @RunWith(AndroidJUnit4::class)
  class SortBenchmark {
      @get:Rule val benchmarkRule = BenchmarkRule()

      @Test fun sortList() {
          val list = (1..1000).shuffled()
          benchmarkRule.measureRepeated {
              list.sorted()
          }
      }
  }
  ```
- **How Claude Code can use it:** Write microbenchmarks for performance-critical code paths. Run before and after optimizations to quantify improvement. Useful for validating that a refactoring does not introduce performance regressions in hot paths.

### JankStats

- **Link:** [developer.android.com/topic/performance/jankstats](https://developer.android.com/topic/performance/jankstats)
- **Description:** Runtime library for detecting janky frames in production and development. Built on `FrameMetrics` API (Android 7+). Defines jank as a frame taking 2x the refresh rate duration. Provides a state API for contextualizing jank — attach UI state labels (e.g., "scrolling list", "opening drawer") so jank reports include what the user was doing. Works with Compose via `PerformanceMetricsState`.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  implementation("androidx.metrics:metrics-performance:1.0.0-beta01")
  ```
  ```kotlin
  // In Activity or Compose:
  val jankStats = JankStats.createAndTrack(window) { frameData ->
      if (frameData.isJank) {
          Log.w("Jank", "Janky frame: ${frameData.frameDurationUiNanos}ns " +
              "states: ${frameData.states}")
      }
  }
  ```
- **How Claude Code can use it:** Integrate JankStats into debug builds to monitor frame performance during manual testing. The state API helps correlate jank with specific UI operations. In CI, combine with Macrobenchmark's `FrameTimingMetric` for automated jank detection.

### Compose Compiler Metrics

- **Link:** [developer.android.com/develop/ui/compose/performance/stability/diagnose](https://developer.android.com/develop/ui/compose/performance/stability/diagnose)
- **Description:** The Compose compiler can output stability reports showing which composables are skippable (efficiently recomposable) vs. restartable-but-not-skippable (always recompose). Generates three report types: class stability report, composable restartability/skippability report, and a CSV version. Helps identify unnecessary recompositions caused by unstable parameters.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts
  composeCompiler {
      reportsDestination = layout.buildDirectory.dir("compose_reports")
      metricsDestination = layout.buildDirectory.dir("compose_metrics")
  }
  ```
  ```bash
  ./gradlew assembleRelease
  # Reports generated in build/compose_reports/ and build/compose_metrics/
  ```
- **How Claude Code can use it:** After modifying composables or data classes, run the compiler metrics and check for regressions in skippability. If a previously-skippable composable becomes non-skippable, investigate whether parameter types became unstable (mutable collections, non-data classes). This is a static analysis — no device needed.

### Layout Inspector (Recomposition Tracking)

- **Link:** [developer.android.com/develop/ui/compose/tooling/debug](https://developer.android.com/develop/ui/compose/tooling/debug)
- **Description:** Android Studio tool that shows the Compose component tree with recomposition counts and skip counts for each node. Highlights actively recomposing nodes with a gradient overlay — higher recomposition rates show stronger highlighting. Helps visually identify which composables are recomposing unnecessarily.
- **Loop phase:** verify
- **How Claude Code can use it:** Layout Inspector is an Android Studio GUI tool — not directly invokable from Claude Code. However, Claude Code can analyze Compose compiler metrics (see above) to detect the same stability issues that Layout Inspector visualizes. For hands-on debugging, recommend the developer use Layout Inspector to observe recomposition behavior in real time.

### Baseline Profiles

- **Link:** [developer.android.com/topic/performance/baselineprofiles](https://developer.android.com/topic/performance/baselineprofiles)
- **Description:** Baseline Profiles tell the Android runtime (ART) which code paths to pre-compile, improving startup time and reducing jank during critical user journeys. Generated by Macrobenchmark test runs that exercise key flows. The profile is bundled in the APK/AAB and used during installation.
- **Loop phase:** verify
- **Install/usage:**
  ```kotlin
  // build.gradle.kts (app module)
  plugins {
      id("androidx.baselineprofile")
  }
  // In benchmark module:
  @RunWith(AndroidJUnit4::class)
  class BaselineProfileGenerator {
      @get:Rule val rule = BaselineProfileRule()

      @Test fun generate() = rule.collect("com.example.app") {
          startActivityAndWait()
          // Exercise critical user flows...
      }
  }
  ```
  ```bash
  ./gradlew :app:generateBaselineProfile
  ```
- **How Claude Code can use it:** Generate baseline profiles after adding new screens or critical flows. Verify profile effectiveness by running Macrobenchmarks with and without the profile. Include `generateBaselineProfile` in the CI pipeline to keep profiles up to date.

---

## Sources

- [Paparazzi — GitHub](https://github.com/cashapp/paparazzi)
- [Compose Preview Screenshot Testing — Android Developers](https://developer.android.com/studio/preview/compose-screenshot-testing)
- [Roborazzi — GitHub](https://github.com/takahirom/roborazzi)
- [Showkase — GitHub](https://github.com/airbnb/Showkase)
- [ComposablePreviewScanner — GitHub](https://github.com/sergio-sastre/ComposablePreviewScanner)
- [Shot — GitHub](https://github.com/pedrovgs/Shot)
- [Dropshots — GitHub](https://github.com/dropbox/dropshots)
- [Android-Testify — GitHub](https://github.com/ndtp/android-testify)
- [Compose Testing — Android Developers](https://developer.android.com/develop/ui/compose/testing)
- [Espresso — Android Developers](https://developer.android.com/training/testing/espresso/basics)
- [UI Automator — Android Developers](https://developer.android.com/training/testing/other-components/ui-automator)
- [Accessibility Checking — Android Developers](https://developer.android.com/training/testing/espresso/accessibility-checking)
- [Compose Semantics — Android Developers](https://developer.android.com/develop/ui/compose/testing/semantics)
- [Screenshotbot](https://screenshotbot.io/)
- [Applitools](https://applitools.com/)
- [Visual Regression Tracker — GitHub](https://github.com/Visual-Regression-Tracker/Visual-Regression-Tracker)
- [Macrobenchmark — Android Developers](https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview)
- [JankStats — Android Developers](https://developer.android.com/topic/performance/jankstats)
- [Compose Compiler Metrics — Android Developers](https://developer.android.com/develop/ui/compose/performance/stability/diagnose)
- [Baseline Profiles — Android Developers](https://developer.android.com/topic/performance/baselineprofiles)
- [Relay — Material.io](https://relay.material.io/)
- [Comparing Snapshot Testing Libraries — Medium](https://medium.com/@natalia.kulbaka/comparing-snapshot-testing-libraries-paparazzi-roborazzi-compose-previews-screenshot-testing-b7c3b47f7f59)
- [Android Screenshot Testing Playground — GitHub](https://github.com/sergio-sastre/Android-screenshot-testing-playground)
- [Droidcon: Master Screenshot Testing](https://academy.droidcon.com/course/master-screenshot-testing-on-android-comparing-paparazzi-roborazzi-and-compose-preview-tools)

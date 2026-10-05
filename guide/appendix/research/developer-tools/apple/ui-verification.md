---
id: ba32d761-5ddd-4883-b230-dde1362a55f5
title: Apple UI Verification Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/apple/ui-verification
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Apple UI Verification Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Apple UI Verification Tools

**Date:** 2026-03-29
**Context:** UI verification and visual testing tools for Apple platforms (SwiftUI, UIKit, AppKit), integrated with Claude Code workflows.

---

## Snapshot Testing (verify)

### swift-snapshot-testing (Point-Free)

- **Link:** [github.com/pointfreeco/swift-snapshot-testing](https://github.com/pointfreeco/swift-snapshot-testing)
- **Description:** The de facto snapshot testing library for Swift. Supports dozens of strategies beyond just image comparison -- text dumps, JSON, plist, cURL, recursive view descriptions, and custom formats. Works with any value that conforms to a snapshotting strategy.
- **Platforms:** iOS, macOS, tvOS, Linux (image strategies require iOS/macOS/tvOS)
- **Install:**
  ```swift
  // Package.swift
  dependencies: [
    .package(url: "https://github.com/pointfreeco/swift-snapshot-testing", from: "1.17.0"),
  ]
  // Add "SnapshotTesting" to test target dependencies only
  ```

#### Available Strategies

| Type | Strategy | Output | Platforms |
|---|---|---|---|
| `Any` | `.description` | String | All |
| `Any` | `.dump` | String (sanitized mirror) | All |
| `CALayer` | `.image` | UIImage/NSImage | iOS, macOS, tvOS |
| `CGPath` | `.image` | UIImage/NSImage | iOS, macOS, tvOS |
| `CGPath` | `.elementsDescription` | String | iOS, macOS, tvOS |
| `Encodable` | `.json` | String (JSON) | All |
| `Encodable` | `.plist` | String (XML plist) | All |
| `NSView` | `.image` | NSImage | macOS |
| `NSView` | `.recursiveDescription` | String | macOS |
| `NSViewController` | `.image` | NSImage | macOS |
| `NSViewController` | `.recursiveDescription` | String | macOS |
| `UIView` | `.image` | UIImage | iOS, tvOS |
| `UIView` | `.recursiveDescription` | String | iOS, tvOS |
| `UIViewController` | `.image` | UIImage | iOS, tvOS |
| `UIViewController` | `.hierarchy` | String | iOS, tvOS |
| `UIViewController` | `.recursiveDescription` | String | iOS, tvOS |
| `UIImage` | `.image` | UIImage | iOS, tvOS |
| `NSImage` | `.image` | NSImage | macOS |
| `UIBezierPath` | `.image` / `.elementsDescription` | UIImage / String | iOS, tvOS |
| `NSBezierPath` | `.image` / `.elementsDescription` | NSImage / String | macOS |
| `SCNScene` | `.image` | UIImage/NSImage | iOS, macOS, tvOS |
| `SKScene` | `.image` | UIImage/NSImage | iOS, macOS, tvOS |
| `String` | `.lines` | String (line diff) | All |
| `URLRequest` | `.curl` | String | All |
| `URLRequest` | `.raw` | String | All |
| `CaseIterable` | `.func(into:)` | CSV | All |

#### Key Configuration

- **Record mode:** Set `isRecording = true` globally or per-test to regenerate reference snapshots. As of 1.17, use `withSnapshotTesting(record: .all)` or `withSnapshotTesting(record: .failed)`.
- **Precision:** Image strategies accept a `precision` parameter (0.0-1.0, default 1.0) for fuzzy matching.
- **Device simulation:** Render on a specific device without needing that simulator: `.image(on: .iPhoneSe)`, `.image(on: .iPadPro12_9)`.
- **Trait collections:** Override size classes, content size categories, and layout direction.
- **Snapshot directory:** Defaults to `__Snapshots__` alongside the test file. Override with `snapshotDirectory` parameter.

#### CI Considerations

- Reference images are committed to the repo alongside test files.
- Image snapshots are pixel-sensitive to OS version, simulator model, and scale factor. Pin CI to a specific Xcode/simulator version.
- Text-based strategies (`.dump`, `.recursiveDescription`, `.json`) are more portable across environments than image strategies.
- Set `SNAPSHOT_ARTIFACTS` environment variable to export failed snapshot diffs to a CI artifacts directory.

#### Claude Code Usage

- Add snapshot tests in a test target. Run with `swift test` or `xcodebuild test`.
- Use `.dump` or `.recursiveDescription` strategies when Claude Code cannot view images -- these produce text diffs readable in the terminal.
- Set `isRecording = true` to regenerate baselines after intentional UI changes.

---

## UI Testing with XCUITest (verify)

### XCUITest (Apple Framework)

- **Link:** [developer.apple.com/documentation/xctest/ui_testing](https://developer.apple.com/documentation/xctest/ui_tests)
- **Description:** Apple's first-party UI testing framework built into XCTest. Tests run in a separate process from the app, interacting through accessibility APIs. Supports element queries, gestures, screenshots, and assertions.
- **Platforms:** iOS, macOS, tvOS, watchOS (limited), visionOS

#### Core Classes

| Class | Purpose |
|---|---|
| `XCUIApplication` | Proxy to launch, monitor, and terminate the app under test |
| `XCUIElement` | Represents a single UI element; supports taps, swipes, typing, value assertions |
| `XCUIElementQuery` | Queries for elements by type, identifier, predicate, or index |
| `XCUIScreen` | Represents a physical screen; used for screenshots |
| `XCUIScreenshot` | A captured image of a screen, app, or element |
| `XCTAttachment` | Wraps screenshots or data for inclusion in test results |

#### Element Queries

```swift
let app = XCUIApplication()
app.launch()

// By accessibility identifier
let button = app.buttons["submitButton"]

// By label text
let label = app.staticTexts["Welcome"]

// By predicate
let cells = app.cells.matching(NSPredicate(format: "label CONTAINS 'Item'"))

// Descendants of any type (useful for SwiftUI)
let element = app.descendants(matching: .any)["myIdentifier"]
```

#### Gestures

```swift
element.tap()
element.doubleTap()
element.press(forDuration: 1.0)
element.swipeUp()
element.swipeDown()
element.swipeLeft()
element.swipeRight()
element.pinch(withScale: 2.0, velocity: 1.0)  // iOS only
element.rotate(0.5, withVelocity: 1.0)         // iOS only
element.typeText("Hello")
```

#### Screenshots in Tests

```swift
let screenshot = app.screenshot()
let attachment = XCTAttachment(screenshot: screenshot)
attachment.name = "Home Screen"
attachment.lifetime = .keepAlways
add(attachment)
```

#### Test Plans

- Configure parallel testing, language/locale overrides, and environment variables via `.xctestplan` files in Xcode.
- Parallel testing distributes test classes across multiple simulator clones.
- Enable in scheme settings or via `xcodebuild test -parallel-testing-enabled YES`.

#### Claude Code Usage

- Run tests: `xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16' -only-testing:MyUITests`
- Extract results: `xcresulttool get --path path/to/Test.xcresult --format json`
- Screenshots from test results appear as XCTAttachments in the xcresult bundle.

---

## SwiftUI Preview Testing (verify)

### PreviewSnapshots (DoorDash)

- **Link:** [github.com/doordash-oss/swiftui-preview-snapshots](https://github.com/doordash-oss/swiftui-preview-snapshots)
- **Description:** Reuse the same view configurations for both Xcode Previews and snapshot tests. Define states once, use them everywhere. Built on top of swift-snapshot-testing.
- **Platforms:** iOS, macOS (wherever SwiftUI Previews work)
- **Install:**
  ```swift
  .package(url: "https://github.com/doordash-oss/swiftui-preview-snapshots", from: "1.0.0")
  // Products: "PreviewSnapshots" (main target), "PreviewSnapshotsTesting" (test target)
  ```

#### Usage

```swift
// In your PreviewProvider:
struct MyView_Previews: PreviewProvider {
    static var snapshots: PreviewSnapshots<String> {
        PreviewSnapshots(
            configurations: [
                .init(name: "Default", state: "Hello"),
                .init(name: "Long Text", state: "A very long string"),
            ],
            configure: { state in MyView(text: state) }
        )
    }

    static var previews: some View {
        snapshots.previews
    }
}

// In your test file:
func testMyView() {
    MyView_Previews.snapshots.assertSnapshots()
}
```

#### Limitation

Does not work with the `#Preview` macro (only `PreviewProvider`).

---

### Prefire

- **Link:** [github.com/BarredEwe/Prefire](https://github.com/BarredEwe/Prefire)
- **Description:** Automatically generates snapshot tests, playbook views, and accessibility tests from `#Preview` blocks and `PreviewProvider` declarations. Uses swift-snapshot-testing under the hood. Build plugin -- no manual test writing needed.
- **Platforms:** iOS 14+, Swift 5.6+, Xcode 14+
- **Install:**
  ```swift
  .package(url: "https://github.com/BarredEwe/Prefire.git", from: "5.4.0")
  // Add "Prefire" and "PrefireTestsPlugin" to test target
  ```

#### How It Works

1. Parses all source files for `#Preview` and `PreviewProvider` blocks at build time
2. Caches parsed results using SHA-256 fingerprints (only re-parses changed files)
3. Generates snapshot test code via Stencil templates
4. Optionally generates a Playbook view for browsing all UI components in-app

#### Configuration (`.prefire.yml`)

```yaml
test_configuration:
  target: MyApp
  snapshot_devices:
    - iPhone 16
    - iPad Pro 13-inch

playbook_configuration:
  preview_default_enabled: true
```

#### Preview Modifiers

```swift
#Preview {
    MyView()
        .prefireEnabled()        // Include in generated tests
        .previewUserStory("Login") // Group in playbook
        .previewState("Error")   // Label the state
}
```

#### Claude Code Usage

- After adding Prefire, run `swift build` to trigger code generation, then `swift test` to run generated snapshot tests.
- The Playbook view (`PlaybookView`) provides an in-app component gallery.

---

### SnapshotPreviews (Emerge Tools)

- **Link:** [github.com/EmergeTools/SnapshotPreviews](https://github.com/EmergeTools/SnapshotPreviews)
- **Description:** Zero-code snapshot testing from Xcode previews. Discovers all `#Preview` and `PreviewProvider` declarations automatically by parsing Mach-O binary metadata. Generates XCTest tests at runtime. Also provides an in-app Preview Gallery and accessibility audits.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS
- **Install:**
  ```swift
  .package(url: "https://github.com/AliSoftware/SnapshotPreviews-iOS", from: "1.0.0")
  // "PreviewGallery" for app target, "SnapshottingTests" for test target
  ```

#### Key Features

| Feature | Description |
|---|---|
| **SnapshotTest** | Base class for auto-generating PNG snapshots from all discovered previews |
| **PreviewGallery** | Interactive browsable gallery of all previews, usable inside the app |
| **AccessibilityPreviewTest** | Runs VoiceOver audits on previews with configurable audit types |
| **Filtering** | Override methods to include/exclude specific previews |

#### Claude Code Usage

- Subclass `SnapshotTest` in your test target -- no manual test methods needed.
- Run with `xcodebuild test` to generate snapshots for every preview in the project.

---

## Accessibility Testing (verify)

### performAccessibilityAudit (XCTest, Apple)

- **Link:** [WWDC23: Perform accessibility audits for your app](https://developer.apple.com/videos/play/wwdc2023/10035/)
- **Description:** Built-in XCTest method (Xcode 15+) that audits any `XCUIElement` for accessibility issues. Fails the test automatically when issues are found. Scoped audits let you check the entire app, a single screen, or an individual component.
- **Platforms:** iOS, macOS, tvOS, visionOS

#### Usage

```swift
// Basic audit -- checks everything on screen
func testAccessibility() throws {
    let app = XCUIApplication()
    app.launch()
    try app.performAccessibilityAudit()
}

// Scoped audit with category filter and known-issue suppression
func testAccessibilityFiltered() throws {
    let app = XCUIApplication()
    app.launch()
    try app.performAccessibilityAudit(for: [.dynamicType, .contrast]) { issue in
        // Ignore known issue on a specific element
        if let element = issue.element,
           element.label == "decorativeImage",
           issue.auditType == .contrast {
            return true  // true = ignore this issue
        }
        return false
    }
}
```

#### Audit Categories

| Category | What It Checks |
|---|---|
| `.dynamicType` | Text scales properly with Dynamic Type settings |
| `.contrast` | Sufficient color contrast ratios |
| `.elementDetection` | Elements are properly exposed to accessibility |
| `.hitRegion` | Touch targets meet minimum size requirements |
| `.sufficientElementDescription` | Elements have meaningful labels |
| `.textClipped` | Text is not clipped or truncated |
| `.trait` | Correct accessibility traits assigned |

#### Limitations

- Only audits elements currently visible on screen. Navigate to each view and audit separately.
- Does not replace manual VoiceOver testing -- supplements it.

---

### Accessibility Inspector (Xcode Tool)

- **Link:** [developer.apple.com/documentation/accessibility](https://developer.apple.com/documentation/accessibility)
- **Description:** Xcode's built-in tool for inspecting accessibility properties of any element in the simulator or on-device. Shows labels, values, traits, and hierarchy. Includes a one-click audit that runs the same checks as `performAccessibilityAudit`.
- **Platforms:** iOS, macOS, tvOS, watchOS, visionOS (via simulator or device)

#### CLI Usage

```bash
# Open Accessibility Inspector
open -a "Accessibility Inspector"

# Accessibility Inspector is GUI-only, but the audit categories
# it exposes are the same ones available in performAccessibilityAudit()
```

#### Claude Code Usage

- Use `performAccessibilityAudit()` in XCTest for automated checks.
- Accessibility Inspector is a GUI tool -- not directly usable from Claude Code. Instead, rely on XCTest audit methods and `XCUIElement` property assertions:

```swift
XCTAssertEqual(element.label, "Submit Order")
XCTAssertTrue(element.isEnabled)
XCTAssertNotNil(element.value)
```

---

### AccessibilityPreviewTest (Emerge Tools)

- **Link:** Part of [SnapshotPreviews](https://github.com/EmergeTools/SnapshotPreviews)
- **Description:** Runs VoiceOver accessibility audits on all discovered Xcode previews. Subclass `AccessibilityPreviewTest` to automatically audit every preview in your project.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS

---

### WWDC25: Record, Replay, and Review

- **Link:** [WWDC25 Session 344](https://developer.apple.com/videos/play/wwdc2025/344/)
- **Description:** New Xcode 17 UI automation features for recording, replaying, and reviewing UI interactions. Includes improved accessibility-driven automation and stable element identification for SwiftUI views.
- **Platforms:** iOS, macOS, visionOS

---

## Visual Regression (verify)

### Screenshotbot

- **Link:** [screenshotbot.io](https://screenshotbot.io/)
- **Description:** Cloud-hosted visual regression service for iOS, Android, and web. Integrates with CI to compare screenshots across builds, posting diff reports to pull requests (GitHub, GitLab). Stores screenshot history -- no Git LFS needed.
- **Platforms:** iOS, Android, Web (screenshot source agnostic)

#### CI Integration

1. Generate screenshots via swift-snapshot-testing or XCUITest
2. Call the Screenshotbot CLI in CI to upload screenshots
3. Screenshotbot compares against the base branch and posts a PR comment with visual diffs

#### Claude Code Usage

- Review Screenshotbot PR comments for visual regressions.
- Not directly invocable from Claude Code -- operates in CI.

---

### Applitools Eyes

- **Link:** [applitools.com](https://applitools.com/)
- **Description:** AI-powered visual testing platform. Uses Visual AI to detect meaningful visual differences while ignoring rendering noise. Supports design-to-code comparison via Figma plugin. Eyes 10.22 added Storybook and Figma design validation.
- **Platforms:** iOS (via Appium/XCUITest), Android, Web
- **Pricing:** Commercial (free tier available)

#### Figma Integration

- Export Figma frames as baselines via the Eyes Figma Plugin.
- Compare live app screenshots against design baselines.
- Visual AI flags meaningful differences, ignoring minor rendering shifts.

---

### Percy (BrowserStack)

- **Link:** [percy.io](https://percy.io/)
- **Description:** Visual review platform that captures and compares screenshots across builds. App Percy extends support to native iOS and Android apps on real devices.
- **Platforms:** iOS, Android, Web
- **Pricing:** Commercial (free tier for open source)

---

### xcparse (Screenshot Extraction)

- **Link:** [github.com/ChargePoint/xcparse](https://github.com/ChargePoint/xcparse)
- **Description:** Command-line tool for extracting screenshots and code coverage data from Xcode `.xcresult` bundles. Essential for CI pipelines that need to post-process test screenshots.
- **Platforms:** macOS (processes results from any Apple platform test run)
- **Install:**
  ```bash
  brew install chargepoint/xcparse/xcparse
  ```

#### Usage

```bash
# Extract all screenshots from a test result
xcparse screenshots /path/to/Test.xcresult /output/directory

# Filter by test status (only failed tests)
xcparse screenshots --test-status "Failure" /path/to/Test.xcresult /output/directory

# Filter by activity type
xcparse screenshots --activity-type "com.apple.dt.xctest.activity-type.userCreated" /path/to/Test.xcresult /output/directory

# Extract code coverage
xcparse codecov /path/to/Test.xcresult /output/directory
```

#### Note

Uses `--legacy` flag for Xcode 16+ where some `xcresulttool` commands were deprecated.

#### Claude Code Usage

- Run `xcparse screenshots` after `xcodebuild test` to extract screenshots for review.
- Combine with image diff tools for automated visual regression in CI.

---

## Screenshot Capture and Comparison (verify)

### xcrun simctl (Simulator CLI)

- **Link:** Built into Xcode Command Line Tools
- **Description:** Apple's command-line interface for interacting with iOS Simulator. Captures screenshots and records video directly from the simulator process.
- **Platforms:** iOS, watchOS, tvOS, visionOS (all simulator-based platforms)

#### Screenshot Commands

```bash
# Capture screenshot of booted simulator
xcrun simctl io booted screenshot screenshot.png

# Specify format (png, tiff, bmp, gif, jpeg)
xcrun simctl io booted screenshot --type=jpeg screenshot.jpg

# Record video
xcrun simctl io booted recordVideo video.mp4

# Override status bar for clean screenshots
xcrun simctl status_bar booted override --time "9:41" --batteryState charged --batteryLevel 100

# Reset status bar
xcrun simctl status_bar booted clear
```

#### Claude Code Usage

- Capture screenshots directly: `xcrun simctl io booted screenshot /tmp/screen.png`
- Override status bar before screenshot for consistent CI images.
- Combine with diff tools for before/after comparison.

---

### XCUIScreenshot and XCTAttachment (XCTest)

- **Link:** [developer.apple.com/documentation/xctest/xcuiscreenshot](https://developer.apple.com/documentation/xctest/xcuiscreenshot)
- **Description:** XCTest APIs for capturing screenshots during UI test execution and attaching them to test results. Screenshots persist in the `.xcresult` bundle.
- **Platforms:** iOS, macOS, tvOS, visionOS

#### Usage in Tests

```swift
// Capture app screenshot
let screenshot = XCUIApplication().screenshot()

// Capture specific screen
let screen = XCUIScreen.main.screenshot()

// Attach to test results with permanent retention
let attachment = XCTAttachment(screenshot: screenshot)
attachment.name = "Login Screen - Dark Mode"
attachment.lifetime = .keepAlways  // .deleteOnSuccess is default
add(attachment)
```

#### Automated Screenshots with Test Plans

- Use `.xctestplan` files to configure screenshot capture across multiple locales and devices.
- Each test plan configuration runs the same tests with different settings, generating screenshots for every combination.

---

### MCP iOS Simulator Screenshot

- **Link:** [github.com/yorifuji/mcp-ios-simulator-screenshot](https://glama.ai/mcp/servers/@yorifuji/mcp-ios-simulator-screenshot)
- **Description:** MCP server that captures iOS Simulator screenshots and saves them to a specified directory. Lightweight, single-purpose tool.
- **Platforms:** iOS Simulator
- **Install:**
  ```json
  {
    "mcpServers": {
      "ios-simulator-screenshot": {
        "command": "npx",
        "args": ["-y", "@anthropic/mcp-ios-simulator-screenshot", "--output-dir", "/tmp/screenshots"]
      }
    }
  }
  ```
- **Requirements:** Node.js >= 18, Xcode with simulator

#### Claude Code Usage

- Directly captures simulator screenshots through MCP tool calls.
- Screenshots saved to configured output directory for comparison.

---

### iOS Simulator MCP (Whitesmith)

- **Link:** [github.com/whitesmith/ios-simulator-mcp](https://github.com/whitesmith/ios-simulator-mcp)
- **Description:** Full-featured MCP server for iOS Simulator interaction. Screenshots, UI hierarchy inspection, tap/swipe/type gestures, app management, GPS simulation. Uses IDB (Facebook's iOS Development Bridge) under the hood.
- **Platforms:** iOS Simulator
- **Install:**
  ```bash
  # Prerequisites
  xcode-select --install
  brew install idb-companion
  pipx install fb-idb --python python3.11

  # Clone and setup
  git clone https://github.com/whitesmith/ios-simulator-mcp.git
  cd ios-simulator-mcp && uv sync
  ```

#### Capabilities

| Tool | Description |
|---|---|
| `screenshot` | Captures JPEG screenshot (~2MB max), returns image for visual inspection |
| `get_ui_hierarchy` | Returns accessibility tree with element positions and labels |
| `tap` | Tap at x,y coordinates |
| `swipe` | Swipe between two points |
| `type_text` | Type text into focused field |
| `tap_and_type` | Combined tap-to-focus then type |
| `press_button` | Hardware buttons (home, lock, volume) |
| `launch_app` / `terminate_app` | App lifecycle control |
| `set_location` | GPS coordinate simulation |

#### Claude Code Usage

- Inspect UI hierarchy to verify element placement and accessibility labels.
- Capture screenshots after interactions for visual verification.
- Automate tap/swipe sequences for end-to-end testing.

---

### XcodeBuildMCP

- **Link:** [xcodebuildmcp.com](https://www.xcodebuildmcp.com/)
- **Description:** Comprehensive MCP server giving AI agents full control over Xcode. 59+ tools covering building, testing, debugging (LLDB), simulator interaction, and deployment. Auto-detects schemes and simulators.
- **Platforms:** iOS, macOS, watchOS, tvOS, visionOS
- **Install:**
  ```json
  {
    "mcpServers": {
      "XcodeBuildMCP": {
        "command": "npx",
        "args": ["-y", "xcodebuildmcp@latest", "mcp"]
      }
    }
  }
  ```

#### Key Verification Tools

| Capability | Description |
|---|---|
| Build and test | Run `xcodebuild test` with automatic error detection |
| Screenshot capture | Capture simulator screenshots during test runs |
| LLDB debugging | Set breakpoints, inspect variables, step through code |
| UI automation | Tap, swipe, interact with simulator UI |
| Scheme detection | Auto-discovers available schemes and destinations |

#### Claude Code Usage

- Build, test, and debug Apple platform projects entirely through MCP tool calls.
- Capture screenshots and inspect UI state without leaving the Claude Code session.
- Attach LLDB debugger to investigate UI rendering issues.

---

## Design Verification (verify)

### Applitools Eyes Figma Plugin

- **Link:** [applitools.com/docs/eyes/integrations/design-validation/figma-plugin](https://applitools.com/docs/eyes/integrations/design-validation/figma-plugin)
- **Description:** Export Figma frames as visual baselines, then compare live app screenshots against them. Visual AI detects meaningful differences, filtering out rendering noise and anti-aliasing artifacts.
- **Platforms:** Any (Figma source, app screenshots from any platform)
- **Pricing:** Commercial

#### Workflow

1. Designer exports Figma frames to Applitools Eyes
2. Developer runs app, captures screenshots (XCUITest, simulator, or manual)
3. Eyes compares screenshots to Figma baselines
4. AI flags meaningful differences (layout shifts, color changes, missing elements)
5. Review and approve/reject in the Eyes dashboard

---

### Apple iOS Design Kit for Figma

- **Link:** [figma.com/community](https://www.figma.com/community/file/1527721578857867021/ios-and-ipados-26)
- **Description:** Apple's official Figma UI kit for iOS and iPadOS 26 (updated March 2026). Includes Liquid Glass components, system controls, and layout templates. Use as a reference to verify your app matches system design patterns.
- **Platforms:** iOS, iPadOS

---

### Manual Design Verification Approach

When automated tools are unavailable or impractical:

1. **Screenshot capture:** `xcrun simctl io booted screenshot design-check.png`
2. **Side-by-side comparison:** Open Figma design and screenshot together
3. **Overlay diff:** Use image editing tools to overlay at 50% opacity
4. **Checklist verification:**
   - Layout spacing and alignment
   - Typography (font, size, weight, line height)
   - Color accuracy (sample with color picker)
   - Touch target sizes (minimum 44x44pt)
   - Dark mode / light mode variants
   - Dynamic Type at all sizes
   - Safe area compliance

#### Claude Code Usage

- Capture simulator screenshots and describe expected layout.
- Use text-based snapshot strategies (`.dump`, `.recursiveDescription`) to verify view hierarchy matches expectations.
- For projects with the Figma Claude Code plugin installed, use `figma-implement-design` skill's built-in validation checklist (Step 7) to verify layout, typography, colors, interactive states, responsive behavior, and accessibility.

---

## Performance UI Testing (verify)

### XCTMetric Framework (Apple)

- **Link:** [developer.apple.com/documentation/xctest/xctmetric](https://developer.apple.com/documentation/xctest/xctmetric)
- **Description:** XCTest performance measurement framework. Wrap code in `measure(metrics:)` blocks to collect CPU, memory, storage, timing, and animation metrics. Baselines are stored per-device and Xcode flags regressions automatically.
- **Platforms:** iOS, macOS, tvOS, watchOS, visionOS

#### Available Metrics

| Metric Class | What It Measures |
|---|---|
| `XCTClockMetric` | Wall clock time elapsed |
| `XCTCPUMetric` | CPU cycles, instructions retired, CPU time |
| `XCTMemoryMetric` | Physical memory usage (peak and average) |
| `XCTStorageMetric` | Logical bytes written to storage |
| `XCTApplicationLaunchMetric` | App launch duration (cold and warm) |
| `XCTOSSignpostMetric` | Duration of os_signpost intervals, plus animation-specific metrics |

#### App Launch Time

```swift
func testAppLaunchPerformance() {
    measure(metrics: [XCTApplicationLaunchMetric()]) {
        XCUIApplication().launch()
    }
}
```

#### Scroll Hitch Detection

```swift
func testScrollPerformance() {
    let app = XCUIApplication()
    app.launch()

    let list = app.collectionViews.firstMatch

    measure(metrics: [XCTOSSignpostMetric.scrollDraggingMetric]) {
        list.swipeUp(velocity: .fast)
    }
}
```

#### XCTOSSignpostMetric Scroll/Navigation Presets

| Preset | What It Measures |
|---|---|
| `.scrollDraggingMetric` | Performance during active finger-drag scrolling |
| `.scrollDecelerationMetric` | Performance during scroll deceleration (after finger lift) |
| `.scrollingAndDecelerationMetric` | Combined drag + deceleration |
| `.navigationTransitionMetric` | Duration and smoothness of view transitions |
| `.customNavigationTransitionMetric` | Custom navigation transition performance |

#### Animation Hitch Metrics (via XCTOSSignpostMetric)

When measuring animation signpost intervals, XCTest reports:

| Metric | Description |
|---|---|
| Frame count | Total frames rendered in the interval |
| Frame rate | Average frames per second |
| Hitch count | Number of frames delivered late |
| Hitch total duration | Cumulative late delivery time (ms) |
| Hitch time ratio | Hitch ms per second of animation (target: < 5 ms/s) |

#### Understanding Hitch Severity

| Hitch Time Ratio | Severity |
|---|---|
| < 5 ms/s | Good -- imperceptible to users |
| 5-10 ms/s | Warning -- subtle but detectable |
| > 10 ms/s | Critical -- clearly visible stutter |

#### Core Animation Instruments

For deeper investigation beyond XCTest:

```bash
# Profile with Instruments from command line
xcrun xctrace record --template "Animation Hitches" --device booted --launch -- /path/to/MyApp.app

# Export trace for analysis
xcrun xctrace export --input recording.trace --output /tmp/trace-export
```

#### Claude Code Usage

- Add performance test methods to the UI test target.
- Run with `xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16' -only-testing:MyPerfTests`.
- Xcode stores baselines and flags regressions automatically. Review results via `xcresulttool`.
- For scroll hitch detection, use the signpost metrics in CI to catch frame rate regressions before shipping.

---

## Sources

### Libraries and Frameworks
- [swift-snapshot-testing (Point-Free)](https://github.com/pointfreeco/swift-snapshot-testing)
- [PreviewSnapshots (DoorDash)](https://github.com/doordash-oss/swiftui-preview-snapshots)
- [Prefire](https://github.com/BarredEwe/Prefire)
- [SnapshotPreviews (Emerge Tools)](https://github.com/EmergeTools/SnapshotPreviews)
- [xcparse (ChargePoint)](https://github.com/ChargePoint/xcparse)

### MCP Servers
- [XcodeBuildMCP](https://www.xcodebuildmcp.com/)
- [iOS Simulator MCP (Whitesmith)](https://github.com/whitesmith/ios-simulator-mcp)
- [iOS Simulator MCP (joshuayoes)](https://github.com/joshuayoes/ios-simulator-mcp)
- [MCP iOS Simulator Screenshot](https://glama.ai/mcp/servers/@yorifuji/mcp-ios-simulator-screenshot)

### Visual Regression Services
- [Screenshotbot](https://screenshotbot.io/)
- [Applitools Eyes](https://applitools.com/)
- [Percy (BrowserStack)](https://percy.io/)

### Apple Documentation
- [XCUITest / UI Testing](https://developer.apple.com/documentation/xctest/ui_tests)
- [XCUIScreenshot](https://developer.apple.com/documentation/xctest/xcuiscreenshot)
- [XCTMetric](https://developer.apple.com/documentation/xctest/xctmetric)
- [XCTOSSignpostMetric](https://developer.apple.com/documentation/xctest/xctossignpostmetric)
- [XCTApplicationLaunchMetric](https://developer.apple.com/documentation/xctest/xctapplicationlaunchmetric)
- [Performing Accessibility Testing](https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app)
- [WWDC23: Perform accessibility audits for your app](https://developer.apple.com/videos/play/wwdc2023/10035/)
- [WWDC25: Record, replay, and review](https://developer.apple.com/videos/play/wwdc2025/344/)
- [WWDC20: Eliminate animation hitches with XCTest](https://developer.apple.com/videos/play/wwdc2020/10077/)
- [Apple iOS & iPadOS 26 Figma Kit](https://www.figma.com/community/file/1527721578857867021/ios-and-ipados-26)

### Guides and Tutorials
- [Stop Shipping Visual Bugs: iOS Snapshot Testing Guide (DEV)](https://dev.to/swift_pal/stop-shipping-visual-bugs-complete-ios-snapshot-testing-guide-for-uikit-swiftui-4i5o)
- [Snapshot Testing in iOS (Bitrise)](https://bitrise.io/blog/post/snapshot-testing-in-ios-testing-the-ui-and-beyond)
- [XCUITest for SwiftUI (swiftyplace)](https://www.swiftyplace.com/blog/xcuitest-ui-testing-swiftui)
- [Accessibility Regression Testing with XCUI (DEV)](https://dev.to/steady5063/accessibility-regression-testing-with-xcui-mpa)
- [Performance Testing with XCTest (Augmented Code)](https://augmentedcode.io/2019/12/22/performance-testing-using-xctmetric/)
- [Discovering UI Performance Testing (DEV)](https://dev.to/mtmorozov/discovering-ui-performance-testing-with-xctest-scrolling-performance-pon)
- [Visual Regression Testing in Mobile QA: 2026 Guide](https://www.getpanto.ai/blog/visual-regression-testing-in-mobile-qa)
- [DoorDash: PreviewSnapshots Blog](https://careersatdoordash.com/blog/how-to-speed-up-swiftui-development-and-testing-using-previewsnapshots/)
- [Screenshotbot: SwiftUI Previews and Prefire](https://screenshotbot.io/blog/swiftui-previews-and-prefire-free-snapshot-tests)

---
id: dddcffe6-5366-4f03-9218-73da330877e1
title: Windows UI Verification Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/windows/ui-verification
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Windows UI Verification Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Windows UI Verification Tools

**Date:** 2026-03-29
**Context:** UI verification and visual testing tools for Windows desktop development (WinUI 3, WPF, MAUI), integrated with Claude Code.

---

## Screenshot & Snapshot Testing (verify)

### [Verify (VerifyTests)](https://github.com/VerifyTests/Verify)

Snapshot testing tool for .NET that simplifies assertion of complex data models, documents, and images. The de facto standard for snapshot testing in .NET.

- **Loop phase:** verify
- **Platforms:** WinUI 3, WPF, MAUI, any .NET project
- **Install:** `dotnet add package Verify.Xunit` (or `Verify.NUnit`, `Verify.MSTest`)
- **Image comparison extension:** `dotnet add package Verify.ImageSharp.Compare`
- **How it works:** Captures output (including screenshots) and compares against a `.verified.*` baseline file. On first run, produces a `.received.*` file for approval. Subsequent runs diff against the approved baseline. Integrates with diff tools for visual comparison.
- **Claude Code usage:** Run `dotnet test` and inspect `.received.*` vs `.verified.*` diffs in test output. Claude Code can read diff output to identify which snapshots changed and why. Approve new baselines by copying `.received.*` to `.verified.*`.

### [ApprovalTests.Net](https://github.com/approvals/ApprovalTests.Net)

Approval-based verification library with dedicated WPF and WinForms screenshot extensions.

- **Loop phase:** verify
- **Platforms:** WPF, WinForms
- **Install:**
  ```
  dotnet add package ApprovalTests
  dotnet add package ApprovalTests.Wpf       # WPF screenshot verification
  dotnet add package ApprovalTests.WinForms   # WinForms screenshot verification
  ```
- **How it works:** Takes a screenshot of a WPF/WinForms control, saves it as a `.received.png`, and compares against an `.approved.png` baseline. Uses the system's default diff tool for visual review.
- **Claude Code usage:** Run tests via `dotnet test`. Failures produce `.received.*` files — Claude Code can detect these and report mismatches. Approve baselines via file copy commands.

### [Snapshooter](https://github.com/SwissLife-OSS/snapshooter)

Snapshot testing tool for .NET Core and .NET Framework with JSON-focused comparison.

- **Loop phase:** verify
- **Platforms:** Any .NET project (data snapshots, not visual)
- **Install:** `dotnet add package Snapshooter.Xunit` (or `.NUnit`, `.MSTest`)
- **How it works:** Serializes test output to JSON and compares against stored snapshots. Best for verifying serialized UI state, view models, or configuration rather than visual screenshots.
- **Claude Code usage:** Run `dotnet test` and parse snapshot diff output. Useful for verifying that data backing UI elements hasn't regressed.

---

## UI Automation (verify)

### [FlaUI](https://github.com/FlaUI/FlaUI)

Modern .NET wrapper around Microsoft UI Automation (UIA2 and UIA3). The most actively maintained UI automation library for Windows desktop apps.

- **Loop phase:** verify
- **Platforms:** WinUI 3, WPF, WinForms, UWP, Win32
- **Install:**
  ```
  dotnet add package FlaUI.UIA3    # For WPF, WinUI, Store apps (recommended)
  dotnet add package FlaUI.UIA2    # For legacy WinForms apps
  ```
- **Key capabilities:** Launch apps, find elements by AutomationId/Name/ClassName, click/type/scroll, read property values, capture screenshots, traverse visual/automation trees.
- **Screenshot capture:** `element.Capture()` or `CaptureImage.CaptureScreen()` returns a `Bitmap` for saving or comparison.
- **Claude Code usage:** Write and run FlaUI test projects via `dotnet test`. Claude Code can generate FlaUI test code, run tests, and parse NUnit/xUnit results. FlaUI's element tree queries are scriptable from CLI.

### [FlaUInspect](https://github.com/FlaUI/FlaUInspect)

Visual inspection tool for exploring UI Automation trees of running Windows applications. The modern replacement for Inspect.exe.

- **Loop phase:** verify (interactive)
- **Install:** `choco install flauinspect` or download from [GitHub Releases](https://github.com/FlaUI/FlaUInspect/releases)
- **How it works:** Displays the UIA element hierarchy (visual tree, properties, patterns) for any running Windows app. Supports both UIA2 and UIA3 modes. Hover + Ctrl to inspect any on-screen element.
- **Claude Code usage:** Not directly usable from CLI, but Claude Code can instruct users to run it for element discovery. AutomationId and control type information gathered from FlaUInspect feeds into FlaUI test scripts.

### [Microsoft UI Automation (UIA)](https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/)

The built-in Windows accessibility and automation framework. Ships with .NET Framework and Windows SDK.

- **Loop phase:** verify
- **Platforms:** All Windows UI frameworks
- **Install:** Built into .NET Framework (`UIAutomationClient.dll`). No NuGet package needed for .NET Framework projects. For .NET Core/.NET 5+, use FlaUI as the wrapper.
- **Key APIs:** `AutomationElement`, `TreeWalker`, control patterns (`InvokePattern`, `ValuePattern`, `SelectionPattern`, etc.).
- **Claude Code usage:** Typically accessed through FlaUI rather than directly. Claude Code can generate raw UIA code, but FlaUI provides a cleaner API.

### [WinAppDriver](https://github.com/microsoft/WinAppDriver)

Microsoft's Appium-compatible WebDriver server for Windows app automation. **Note: Development has been paused by Microsoft. Consider alternatives.**

- **Loop phase:** verify
- **Platforms:** UWP, WPF, WinForms, Win32
- **Install:** Download from [GitHub Releases](https://github.com/microsoft/WinAppDriver/releases). Requires Windows 10+ with Developer Mode enabled.
- **Run:** `WinAppDriver.exe` (starts on port 4723)
- **Screenshot:** `driver.GetScreenshot()` via Appium client
- **Claude Code usage:** Start WinAppDriver, run Appium tests via `dotnet test`. Claude Code can generate Appium test code in C#. **Caveat:** No longer maintained — prefer FlaUI or NovaWindows Driver for new projects.

### [NovaWindows Driver (Appium)](https://github.com/AutomateThePlanet/appium-novawindows-driver)

Open-source Appium 2 driver for Windows desktop automation. Drop-in replacement for the abandoned WinAppDriver/Appium Windows driver.

- **Loop phase:** verify
- **Platforms:** UWP, WPF, WinForms, Win32
- **Install:** `appium driver install novawindows`
- **Migration from WinAppDriver:** Change `automationName` capability from `"Windows"` to `"NovaWindows"`.
- **Advantages over WinAppDriver:** Faster XPath locators, RawView element support, enhanced text input handling, smooth mouse movements.
- **Claude Code usage:** Install via Appium CLI, run tests with `dotnet test`. Claude Code can generate Appium test code and migrate existing WinAppDriver tests by updating capabilities.

---

## Accessibility Testing (verify)

### [Accessibility Insights for Windows](https://accessibilityinsights.io/docs/windows/overview/)

Free, open-source Microsoft tool for finding and fixing accessibility issues in Windows apps. The recommended replacement for legacy SDK accessibility tools.

- **Loop phase:** verify
- **Platforms:** All Windows UI frameworks
- **Install:** Download from [accessibilityinsights.io/downloads](https://accessibilityinsights.io/downloads/)
- **Key features:**
  - **Live Inspect** — hover over any element to view its UIA properties
  - **FastPass** — automated scan checking 60+ accessibility requirements in under 5 minutes
  - **Tab stops test** — visual helper for keyboard navigation verification
  - **Color Contrast Analyzer** — eyedropper tool for WCAG color contrast verification
- **Claude Code usage:** Not directly scriptable from CLI. Use the programmatic engine (Axe.Windows) for automated testing. Claude Code can reference FastPass results and guide remediation.

### [Axe.Windows](https://github.com/microsoft/axe-windows)

The programmatic accessibility testing engine that powers Accessibility Insights. Runs automated accessibility scans from code or CLI.

- **Loop phase:** verify
- **Platforms:** All Windows UI frameworks
- **Install:** `dotnet add package Axe.Windows`
- **CLI:** `dotnet tool install --global AxeWindowsCLI`
- **Usage:**
  ```csharp
  var scanner = ScannerFactory.CreateScanner(config);
  var results = scanner.Scan();
  ```
- **CI integration:** Run `axe-windows-cli scan --process-name MyApp.exe` in build pipelines. Results can be saved as `.a11ytest` files openable in Accessibility Insights.
- **Claude Code usage:** Integrate into test projects and run via `dotnet test`. Claude Code can parse scan results, identify failing rules, and suggest XAML/code fixes. The CLI mode is ideal for CI/CD pipelines.

### [Inspect.exe](https://learn.microsoft.com/en-us/windows/win32/winauto/inspect-objects)

Windows SDK tool for viewing UIA properties and MSAA properties of any UI element.

- **Loop phase:** verify (interactive)
- **Install:** Included in Windows SDK (`%ProgramFiles(x86)%\Windows Kits\10\bin\<version>\<platform>\Inspect.exe`)
- **How it works:** Select any UI element to view its automation properties, control patterns, and accessibility information.
- **Claude Code usage:** Not scriptable. Use for manual verification. For automated inspection, use FlaUI or Axe.Windows instead.

### [AccChecker (UI Accessibility Checker)](https://learn.microsoft.com/en-us/windows/win32/winauto/ui-accessibility-checker)

Legacy Windows SDK tool for verifying UIA and MSAA implementations. **Deprecated — use Accessibility Insights or Axe.Windows instead.**

- **Loop phase:** verify
- **Install:** Included in Windows SDK
- **Checks:** UIA compliance, MSAA compliance, ARIA compliance
- **Claude Code usage:** Legacy tool. Prefer Axe.Windows for programmatic accessibility testing.

### [UI Automation Verify (UIA Verify)](https://learn.microsoft.com/en-us/windows/win32/winauto/accessibility-testingtools)

Windows SDK framework for manual and automated testing of UIA implementations.

- **Loop phase:** verify
- **Install:** Included in Windows SDK
- **How it works:** Tests control pattern implementations and UIA tree structure. Can log results for review.
- **Claude Code usage:** Legacy tool. Prefer FlaUI + Axe.Windows for modern automated verification.

---

## Visual Regression (verify)

### [Verify.ImageSharp.Compare](https://github.com/VerifyTests/Verify.ImageSharp.Compare)

Verify extension that adds image comparison using ImageSharp.Compare. Best-in-class for integrating visual regression into .NET test suites.

- **Loop phase:** verify
- **Install:** `dotnet add package Verify.ImageSharp.Compare`
- **How it works:** Captures screenshots (via FlaUI, Appium, or manual save), then uses Verify's snapshot workflow to compare images. Supports pixel-level comparison with configurable thresholds. Produces diff images highlighting changes.
- **Claude Code usage:** Add to test projects alongside FlaUI or Appium screenshot capture. Run `dotnet test` and inspect failures. Claude Code can read test output to identify which screenshots regressed and by how much.

### [ImageSharp.Compare](https://github.com/Codeuctivity/ImageSharp.Compare)

Cross-platform .NET image comparison library. Calculates mean error, absolute error, and generates diff images.

- **Loop phase:** verify
- **Install:** `dotnet add package Codeuctivity.ImageSharpCompare`
- **Key features:**
  - Pixel-level comparison with tolerance masks
  - Mean/absolute error calculation
  - Diff image generation
  - OS-agnostic (runs on Windows, Linux, macOS)
- **Claude Code usage:** Integrate into custom test harnesses. Claude Code can write comparison scripts that capture FlaUI screenshots and compare against baselines using ImageSharpCompare APIs.

### [Visual Regression Tracker](https://github.com/Visual-Regression-Tracker/Visual-Regression-Tracker)

Self-hosted, open-source platform for managing visual regression test results across projects.

- **Loop phase:** verify
- **Install:** Self-hosted via Docker: `docker compose up`
- **SDK:** .NET SDK available via NuGet (`VisualRegressionTracker`)
- **Key features:**
  - Centralized baseline management with approval UI
  - Ignore regions for dynamic content
  - Baseline history tracking
  - Multi-platform support (web, desktop, mobile)
  - No per-screenshot fees
- **Claude Code usage:** Deploy the server, then integrate the .NET SDK into test projects. Claude Code can run tests and check the tracker API for regression results. Suitable for teams running CI with FlaUI or Appium screenshot capture.

### CI Integration Pattern

For any visual regression approach, the standard CI pattern is:

```
1. FlaUI/Appium captures screenshots during test run
2. Comparison library (ImageSharp.Compare or Verify) diffs against baselines
3. Test fails if diff exceeds threshold
4. Review diff images in CI artifacts
5. Approve new baselines when changes are intentional
```

Claude Code can orchestrate this entire pipeline via `dotnet test` and file system inspection.

---

## Design Verification (verify)

### [Windows UI Kit for Figma](https://www.figma.com/community/file/1440832812269040007/windows-ui-kit)

Official Microsoft Figma library with WinUI 3 components, design patterns, colors, typography, and spacing tokens.

- **Loop phase:** verify (design review)
- **How it works:** Designers create screens using the official kit. Developers compare implementation against Figma designs. The kit's components map directly to WinUI 3 controls.
- **Claude Code usage:** Claude Code cannot directly access Figma files, but can verify that XAML implementations use the correct WinUI control types, spacing values, and color tokens that match Fluent Design specifications.

### [Fluent 2 Design System](https://fluent2.microsoft.design/)

Microsoft's cross-platform design system with tokens for color, typography, spacing, and elevation.

- **Loop phase:** verify
- **Design tokens:** Available as Figma variables and in code via WinUI 3 theme resources.
- **Verification approach:** Compare XAML `ThemeResource` usage against Fluent 2 token names. Verify that custom styles don't override Fluent defaults without justification.
- **Claude Code usage:** Claude Code can audit XAML files for correct Fluent resource references (e.g., `{ThemeResource BodyTextBlockStyle}`), flag hardcoded colors/sizes that should use theme resources, and verify control usage against Fluent guidelines.

### [Design System Compliance Checker (Figma Plugin)](https://www.figma.com/community/plugin/1577978298506710437/design-system-compliance-checker)

Figma plugin that audits design files for consistent use of design system styles and components.

- **Loop phase:** verify (design)
- **How it works:** Scans Figma frames for detached styles, non-library components, and inconsistent token usage.
- **Claude Code usage:** Not directly accessible. Results inform what to verify in code — Claude Code can cross-reference compliance findings with XAML implementation.

---

## XAML Analysis (implement/verify)

### [XAML Styler](https://marketplace.visualstudio.com/items?itemName=TeamXavalon.XAMLStyler)

Visual Studio extension that formats XAML source code based on configurable styling rules.

- **Loop phase:** implement
- **Install:** Visual Studio extension or `dotnet tool install --global XamlStyler.Console`
- **CLI usage:** `xstyler --file MyPage.xaml` or `xstyler --directory ./Views`
- **Key features:** Attribute ordering, line breaking rules, indentation normalization, team-shared configuration via `Settings.XamlStyler` file.
- **Claude Code usage:** Run `xstyler` CLI on XAML files after editing. Claude Code can invoke the formatter and verify clean output. Include in pre-commit hooks for consistent XAML formatting.

### [XAML Data Binding Diagnostics (Visual Studio)](https://learn.microsoft.com/en-us/visualstudio/xaml-tools/xaml-data-binding-diagnostics)

Built-in Visual Studio tool that displays binding failures in a dedicated tool window.

- **Loop phase:** verify
- **Platforms:** WPF, UWP, WinUI 3
- **How it works:** The XAML Binding Failures window shows failed bindings with file location, binding path, and failure reason. Allows searching, sorting, and navigating to the failed binding in XAML.
- **Claude Code usage:** Not directly accessible from CLI. However, Claude Code can audit XAML bindings statically by checking that `x:Bind` paths reference existing properties and that `Binding` paths match ViewModel shapes.

### [Live Visual Tree / Live Property Explorer (Visual Studio)](https://learn.microsoft.com/en-us/windows/apps/develop/ui/visual-tree)

Built-in Visual Studio debugging tools for inspecting the runtime XAML visual tree.

- **Loop phase:** verify (interactive)
- **Platforms:** WPF, UWP, WinUI 3, MAUI
- **How it works:** While debugging, open Debug > Windows > Live Visual Tree to see the real-time element hierarchy. Live Property Explorer shows actual runtime property values including resolved bindings and resource values.
- **Enable for WinUI 3:** Tools > Options > Environment > Preview Features > "Enable UI Debugging Tooling for WinUI 3 Projects"
- **Claude Code usage:** Not CLI-accessible. Use for interactive verification during development. For automated tree inspection, use FlaUI's element tree traversal.

### [XAML Hot Reload (Visual Studio)](https://learn.microsoft.com/en-us/visualstudio/xaml-tools/xaml-hot-reload)

Edit XAML while the app is running and see changes applied without restarting.

- **Loop phase:** implement
- **Platforms:** WPF, UWP, WinUI 3, MAUI
- **How it works:** Modify XAML in the editor while debugging; changes apply immediately to the running app. Supports most property changes, new elements, style modifications.
- **Claude Code usage:** Not directly usable from CLI. Useful during interactive development sessions. Claude Code can make XAML edits that the developer applies via Hot Reload.

### [Snoop WPF](https://github.com/snoopwpf/snoopwpf)

Open-source WPF spy utility for browsing the visual tree, logical tree, and automation tree of running WPF applications.

- **Loop phase:** verify (interactive)
- **Install:** `choco install snoop` or download from [GitHub Releases](https://github.com/snoopwpf/snoopwpf/releases)
- **Key features:**
  - Browse visual/logical/automation trees
  - Edit property values at runtime
  - View triggers and data context
  - Set breakpoints on property changes
  - Filter and search the element tree
- **Claude Code usage:** Not CLI-scriptable. Essential for interactive WPF debugging. Claude Code can guide users on what to look for (e.g., "check DataContext on the failing element" or "verify the binding source").

### XAML Compile-Time Validation

WinUI 3 and MAUI support `x:Bind` which provides compile-time binding validation. WPF `{Binding}` is runtime-only.

- **Loop phase:** implement
- **Verification approach:** Use `x:Bind` instead of `{Binding}` where possible — the compiler catches path errors. For WPF, enable binding trace output in diagnostics.
- **Claude Code usage:** Claude Code can refactor `{Binding}` to `x:Bind` where applicable, and run `dotnet build` to catch binding errors at compile time. Claude Code can also add `PresentationTraceSources.TraceLevel=High` to WPF bindings for debugging.

---

## Performance UI Testing (verify)

### [Windows Performance Recorder (WPR)](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder)

ETW-based system-wide performance recording tool. Part of the Windows Assessment and Deployment Kit (ADK).

- **Loop phase:** verify
- **Install:** Included with Windows (`WPR.exe` ships with Windows 8.1+). Full version via [Windows ADK](https://learn.microsoft.com/en-us/windows-hardware/get-started/adk-install).
- **CLI usage:**
  ```
  wpr -start GeneralProfile     # Start recording
  wpr -stop output.etl          # Stop and save trace
  ```
- **XAML Frame Analysis:** Available in ADK 10.1.26100.1+, calculates per-frame duration for XAML apps.
- **Claude Code usage:** Claude Code can script `wpr` to capture traces during automated test runs, then instruct the user to open `.etl` files in WPA for analysis. Useful for CI perf gates (capture trace, check for frame drops).

### [Windows Performance Analyzer (WPA)](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer)

Visual analysis tool for ETW traces captured by WPR. Available standalone from the Microsoft Store.

- **Loop phase:** verify (interactive)
- **Install:** Microsoft Store ("Windows Performance Analyzer") or via Windows ADK
- **Key features:**
  - CPU usage, disk I/O, memory, and GPU analysis
  - XAML Frame Analysis table (ADK 10.1.26100.1+)
  - UI thread utilization graphs
  - Custom graph presets for UI performance scenarios
- **Claude Code usage:** Not CLI-scriptable for analysis. Claude Code can automate trace capture with WPR and instruct users to open specific views in WPA.

### [Visual Studio Application Timeline](https://learn.microsoft.com/en-us/visualstudio/profiling/application-timeline)

Built-in Visual Studio profiler for XAML app resource consumption. Replaced the older "XAML UI Responsiveness" tool.

- **Loop phase:** verify (interactive)
- **Platforms:** WPF, UWP (partial WinUI 3 support)
- **Key features:**
  - Frame-by-frame layout and render timing
  - UI thread utilization
  - Visual throughput (frames per second)
  - Network and disk I/O during UI operations
  - Can pair with CPU Usage tool for method-level analysis
- **Claude Code usage:** Not CLI-accessible. Use during development for identifying slow layouts, expensive renders, and UI thread blocking.

### [dotnet-counters](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-counters)

Cross-platform .NET CLI diagnostic tool for real-time performance monitoring.

- **Loop phase:** verify
- **Install:** `dotnet tool install --global dotnet-counters`
- **Usage:**
  ```
  dotnet-counters monitor --process-id <PID>               # Live monitoring
  dotnet-counters collect --process-id <PID> -o output.csv  # Collect to file
  ```
- **Key counters:** CPU usage, GC heap size, allocation rate, thread pool queue length, exception count, working set.
- **Claude Code usage:** Claude Code can start `dotnet-counters collect` during test runs, then analyze the CSV output for anomalies (e.g., excessive GC, high allocation rate during UI operations).

### [dotnet-trace](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace)

Cross-platform .NET CLI tool for collecting detailed performance traces.

- **Loop phase:** verify
- **Install:** `dotnet tool install --global dotnet-trace`
- **Usage:**
  ```
  dotnet-trace collect --process-id <PID> --providers Microsoft-Windows-XAML
  ```
- **Claude Code usage:** Capture traces during automated test scenarios. Output `.nettrace` files can be converted to `.speedscope.json` for analysis. Claude Code can automate trace collection and flag long-running methods.

---

## MAUI UI Testing (verify)

### [Appium for .NET MAUI](https://learn.microsoft.com/en-us/samples/dotnet/maui-samples/uitest-appium-nunit/)

The officially recommended approach for .NET MAUI UI testing. Uses Appium with platform-specific drivers.

- **Loop phase:** verify
- **Platforms:** Windows (via WinAppDriver or NovaWindows), Android (via UiAutomator2), iOS (via XCUITest), macOS (via Mac2)
- **Install:**
  ```
  npm install -g appium
  appium driver install windows           # or novawindows
  appium driver install uiautomator2      # for Android
  appium driver install xcuitest          # for iOS
  dotnet add package Appium.WebDriver
  ```
- **Screenshot capture:** `driver.GetScreenshot().SaveAsFile("screenshot.png")`
- **Cross-platform test structure:** Share test logic, parameterize by platform driver.
- **Claude Code usage:** Claude Code can generate cross-platform Appium test classes, run tests per-platform via `dotnet test`, and capture/compare screenshots across platforms.

### [Xappium.UITest](https://github.com/Xappium/xappium.uitest)

Higher-level abstraction over Appium specifically designed for cross-platform .NET MAUI testing.

- **Loop phase:** verify
- **Install:** `dotnet add package Xappium.UITest` (currently beta)
- **Test frameworks:** Supports MSTest, NUnit, xUnit via dedicated packages.
- **Key features:** Automatic session management between tests, cross-platform element queries, simplified driver setup.
- **Claude Code usage:** Generate test classes extending `XappiumTestBase`. Run via `dotnet test`. Currently beta — evaluate stability before production use.

### [Plugin.Maui.UITestHelpers](https://www.nuget.org/packages/Plugin.Maui.UITestHelpers.Core/)

Community NuGet package providing MAUI-specific UI test helper methods.

- **Loop phase:** verify
- **Install:** `dotnet add package Plugin.Maui.UITestHelpers.Core` (preview)
- **Claude Code usage:** Add to MAUI test projects for simplified element queries and assertions. Currently preview — evaluate before production use.

### MAUI Visual Regression Pattern

Recommended approach combining tools for MAUI visual regression testing:

```
1. Appium captures screenshots per-platform during test run
2. Verify.ImageSharp.Compare diffs against platform-specific baselines
3. Separate baseline directories per platform:
   baselines/windows/, baselines/android/, baselines/ios/
4. CI matrix runs tests on each platform
5. Visual Regression Tracker (optional) centralizes cross-platform results
```

Claude Code can scaffold this entire structure and generate the test harness code.

---

## Sources

- [Verify (VerifyTests) — GitHub](https://github.com/VerifyTests/Verify)
- [Verify.ImageSharp.Compare — GitHub](https://github.com/VerifyTests/Verify.ImageSharp.Compare)
- [ApprovalTests.Net — GitHub](https://github.com/approvals/ApprovalTests.Net)
- [ApprovalTests.Net.Wpf — GitHub](https://github.com/approvals/ApprovalTests.Net.Wpf)
- [Snapshooter — GitHub](https://github.com/SwissLife-OSS/snapshooter)
- [FlaUI — GitHub](https://github.com/FlaUI/FlaUI)
- [FlaUInspect — GitHub](https://github.com/FlaUI/FlaUInspect)
- [Microsoft UI Automation — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/)
- [WinAppDriver — GitHub](https://github.com/microsoft/WinAppDriver)
- [NovaWindows Driver — GitHub](https://github.com/AutomateThePlanet/appium-novawindows-driver)
- [Accessibility Insights for Windows — Microsoft](https://accessibilityinsights.io/docs/windows/overview/)
- [Axe.Windows — GitHub](https://github.com/microsoft/axe-windows)
- [Inspect.exe — Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/winauto/inspect-objects)
- [AccChecker — Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/winauto/ui-accessibility-checker)
- [ImageSharp.Compare — GitHub](https://github.com/Codeuctivity/ImageSharp.Compare)
- [Visual Regression Tracker — GitHub](https://github.com/Visual-Regression-Tracker/Visual-Regression-Tracker)
- [Windows UI Kit for Figma — Figma Community](https://www.figma.com/community/file/1440832812269040007/windows-ui-kit)
- [Fluent 2 Design System — Microsoft](https://fluent2.microsoft.design/)
- [XAML Styler — Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=TeamXavalon.XAMLStyler)
- [XAML Data Binding Diagnostics — Microsoft Learn](https://learn.microsoft.com/en-us/visualstudio/xaml-tools/xaml-data-binding-diagnostics)
- [Live Visual Tree — Microsoft Learn](https://learn.microsoft.com/en-us/windows/apps/develop/ui/visual-tree)
- [XAML Hot Reload — Microsoft Learn](https://learn.microsoft.com/en-us/visualstudio/xaml-tools/xaml-hot-reload)
- [Snoop WPF — GitHub](https://github.com/snoopwpf/snoopwpf)
- [Windows Performance Recorder — Microsoft Learn](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder)
- [Windows Performance Analyzer — Microsoft Learn](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer)
- [Visual Studio Application Timeline — Microsoft Learn](https://learn.microsoft.com/en-us/visualstudio/profiling/application-timeline)
- [dotnet-counters — Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-counters)
- [Appium for .NET MAUI — Microsoft Learn](https://learn.microsoft.com/en-us/samples/dotnet/maui-samples/uitest-appium-nunit/)
- [Xappium.UITest — GitHub](https://github.com/Xappium/xappium.uitest)
- [Snapshot Testing in .NET with Verify — JetBrains Blog](https://blog.jetbrains.com/dotnet/2024/07/11/snapshot-testing-in-net-with-verify/)
- [WinUI Performance Optimization — Microsoft Learn](https://learn.microsoft.com/en-us/windows/apps/develop/performance/winui-perf)
- [Testing WinUI Apps — Microsoft Learn](https://learn.microsoft.com/en-us/windows/apps/winui/winui3/testing/)
- [Percy Screenshot Testing Guide](https://percy.io/blog/visual-screenshot-testing)

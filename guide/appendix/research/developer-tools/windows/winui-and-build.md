---
id: 0abbafa8-9bbb-4f52-996d-9069ffd4c5d6
title: WinUI, WPF & MAUI Build Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/windows/winui-and-build
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: WinUI, WPF & MAUI Build Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# WinUI, WPF & MAUI Build Tools

**Date:** 2026-03-29
**Context:** Build system and testing tools for Windows UI development with Claude Code. Covers the full plan/implement/verify loop for WinUI 3 (Windows App SDK), WPF, and .NET MAUI desktop targets. All tools are CLI-first and can be invoked from Claude Code via shell-out unless otherwise noted.

**Integration methods:**
- **CLI shell-out** -- Claude Code runs the tool via Bash (most common)
- **MCP server** -- tool exposes a Model Context Protocol server for direct integration
- **Plugin** -- Claude Code plugin bundles LSP, MCP, hooks, or skills

---

## MSBuild CLI (implement/verify)

The `dotnet` CLI wraps MSBuild and is the primary entry point for building, testing, and publishing WinUI, WPF, and MAUI projects from the command line. All commands work headlessly and are safe for Claude Code shell-out.

### dotnet build

- **Link:** https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build
- **What it does:** Compiles the project and its dependencies. For WinUI/WPF/MAUI, the target framework includes a Windows version specifier.
- **Loop phase:** implement
- **Commands:**
  ```
  # WinUI 3 / WPF (.NET 10)
  dotnet build -f net10.0-windows10.0.19041.0 -c Debug

  # .NET MAUI Windows target
  dotnet build -f net10.0-windows10.0.19041.0 -c Debug

  # Specific platform (x64)
  dotnet build -f net10.0-windows10.0.19041.0 -c Debug -r win-x64

  # Scope to a single project (recommended for MAUI solutions)
  dotnet build src/MyApp/MyApp.csproj -f net10.0-windows10.0.19041.0
  ```
- **Claude Code integration:** CLI shell-out. Run after every edit in compiled projects. Exit code 0 means success; non-zero triggers diagnostic review.
- **Notes:** Starting with .NET 8+, version-specific RIDs like `win10-x64` are no longer valid. Use portable RIDs: `win-x64`, `win-x86`, `win-arm64`. For MAUI solutions, always scope `dotnet build` to the app project to avoid building unrelated projects in the solution.

### dotnet publish

- **Link:** https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-publish
- **What it does:** Compiles, packages, and prepares the app for deployment. Supports MSIX (packaged), unpackaged, self-contained, trimmed, and AOT modes.
- **Loop phase:** implement, verify
- **Commands:**
  ```
  # Packaged MSIX (default for WinUI)
  dotnet publish -f net10.0-windows10.0.19041.0 -c Release -r win-x64

  # Unpackaged (no MSIX, plain EXE)
  dotnet publish -f net10.0-windows10.0.19041.0 -c Release -r win-x64 \
    -p:WindowsPackageType=None

  # Self-contained (includes .NET runtime)
  dotnet publish -f net10.0-windows10.0.19041.0 -c Release -r win-x64 \
    --self-contained true

  # Trimmed + self-contained (smaller binary)
  dotnet publish -f net10.0-windows10.0.19041.0 -c Release -r win-x64 \
    --self-contained true -p:PublishTrimmed=true

  # Native AOT (iOS/Mac Catalyst only for MAUI; .NET console/web on Windows)
  dotnet publish -c Release -r win-x64 -p:PublishAot=true
  ```
- **Claude Code integration:** CLI shell-out. Use for final packaging verification.
- **Notes:** MAUI Native AOT (`PublishAot`) targets iOS and Mac Catalyst only. Android uses Mono AOT in .NET 8-10 and CoreCLR in .NET 11+. Windows MAUI/WinUI apps use standard JIT or ReadyToRun. Trimming reduces MAUI app sizes by ~35% but requires all code to be trim-compatible. Always scope `dotnet publish` to the app project, not the solution.

### dotnet run

- **Link:** https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-run
- **What it does:** Builds and runs the project in one step.
- **Loop phase:** implement
- **Commands:**
  ```
  dotnet run --project src/MyApp/MyApp.csproj -f net10.0-windows10.0.19041.0
  ```
- **Claude Code integration:** CLI shell-out. Useful for quick smoke tests, but desktop apps launch a window so the process blocks. Use `--no-build` after a successful build to skip recompilation.

### dotnet msbuild

- **Link:** https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-msbuild
- **What it does:** Provides direct access to MSBuild with full property and target control. Useful when `dotnet build` flags are insufficient.
- **Loop phase:** implement
- **Commands:**
  ```
  # Pass MSBuild properties directly
  dotnet msbuild -p:Configuration=Release -p:Platform=x64 -t:Build

  # Generate MSIX without full publish
  dotnet msbuild -t:Pack -p:Configuration=Release
  ```
- **Claude Code integration:** CLI shell-out. Use when fine-grained MSBuild control is needed beyond what `dotnet build`/`publish` expose.

### dotnet format

- **Link:** https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format
- **What it does:** Formats and applies code-style fixes based on `.editorconfig` and Roslyn analyzer rules. Included in the .NET SDK since v6.
- **Loop phase:** implement, verify
- **Commands:**
  ```
  # Format entire solution
  dotnet format

  # Check only (no writes, exit code 1 if changes needed)
  dotnet format --verify-no-changes

  # Fix analyzer warnings
  dotnet format analyzers --severity warn

  # Fix style issues only
  dotnet format style
  ```
- **Claude Code integration:** CLI shell-out. Run as a verify step after implementation or as a pre-commit check. The `--verify-no-changes` flag is ideal for CI gates.

---

## WinUI Testing (verify)

### WinAppDriver

- **Link:** https://github.com/microsoft/WinAppDriver
- **What it does:** Microsoft's Selenium/Appium-compatible service for automating Windows desktop app UI. Supports UWP, WinUI 3, WPF, WinForms, and Win32. Runs as a local REST service on `http://127.0.0.1:4723/` and accepts WebDriver-protocol commands.
- **Loop phase:** verify
- **Install:**
  ```
  # Download and install the MSI from GitHub releases
  # Service installs to: C:\Program Files (x86)\Windows Application Driver\
  # Launch: WinAppDriver.exe
  ```
- **Claude Code integration:** CLI shell-out (start the service, then run tests via `dotnet test`). Tests use the `Appium.WebDriver` NuGet package and any .NET test framework (xUnit, NUnit, MSTest).
- **Notes:** Development on WinAppDriver has been paused by Microsoft. It still works for existing projects but is not recommended for new projects. Consider FlaUI as the primary alternative. WinAppDriver requires "Developer Mode" enabled in Windows Settings.

### Appium Windows Driver

- **Link:** https://github.com/appium/appium-windows-driver
- **What it does:** Appium's interface to WinAppDriver. Provides the Appium protocol layer on top of WinAppDriver, enabling cross-platform test orchestration. Supports UWP, WPF, WinForms, and Win32 apps on Windows 10+.
- **Loop phase:** verify
- **Install:**
  ```
  # Install Appium server
  npm install -g appium

  # Install Windows driver
  appium driver install windows

  # Add Appium.WebDriver to test project
  dotnet add package Appium.WebDriver
  ```
- **Claude Code integration:** CLI shell-out. Start Appium server, then run tests with `dotnet test`. Tests initialize sessions with `WindowsDriver` specifying app path and platform capabilities.
- **Notes:** Used heavily for .NET MAUI UI testing on Windows. Microsoft's official MAUI testing guidance recommends Appium + NUnit. The `Plugin.Maui.UITestHelpers` NuGet package provides migration helpers from Xamarin.UITest to Appium.

### FlaUI

- **Link:** https://github.com/FlaUI/FlaUI
- **What it does:** .NET UI automation library based on Microsoft's UI Automation (UIA) framework. Supports UIA2 (legacy) and UIA3 (modern, recommended). Works with WPF, WinForms, WinUI 3, and UWP apps. Provides strongly-typed access to UI elements with readable, fluent APIs.
- **Loop phase:** verify
- **Install:**
  ```
  # Add to test project
  dotnet add package FlaUI.UIA3
  dotnet add package FlaUI.Core
  ```
- **Claude Code integration:** CLI shell-out via `dotnet test`. Tests use `Application.Launch()` or `Application.Attach()` to connect to the app, then navigate the visual tree with `AutomationElement` wrappers. Example: `window.FindFirstDescendant(cf => cf.ByAutomationId("myButton")).AsButton().Click()`.
- **Notes:** FlaUI is the strongest UIA-based .NET option for 2025-2026 and the recommended replacement for WinAppDriver and TestStack.White. Use UIA3 for WPF and WinUI 3 apps. Latest release (February 2025) added .NET 8 support. Also available for Robot Framework via `robotframework-flaui` (PyPI, March 2026 release).

---

## WPF Testing (verify)

### FlaUI (WPF-specific usage)

- **Link:** https://github.com/FlaUI/FlaUI
- **What it does:** Same library as above, but WPF has the deepest UIA support. FlaUI can inspect the WPF visual tree, read data bindings, interact with custom controls, and verify MVVM property changes through the UI layer.
- **Loop phase:** verify
- **Install:** `dotnet add package FlaUI.UIA3`
- **Claude Code integration:** CLI shell-out via `dotnet test`. WPF controls expose rich UIA patterns (Invoke, Value, Selection, Toggle, etc.) that FlaUI wraps into strongly-typed methods.
- **Notes:** For BDD-style tests, combine FlaUI with ReqnRoll (Gherkin/BDD for .NET, successor to SpecFlow). FlaUI + ReqnRoll + NUnit is a proven pattern for WPF automation in 2025.

### TestStack.White (archived)

- **Link:** https://github.com/TestStack/White
- **What it does:** Legacy .NET UI automation framework based on UIAutomation. Supported Win32, WinForms, WPF, and Silverlight.
- **Loop phase:** verify
- **Install:** `dotnet add package TestStack.White`
- **Claude Code integration:** CLI shell-out via `dotnet test`.
- **Notes:** **DEPRECATED -- no longer actively maintained.** The last maintainer was unable to add UIA3 support due to architectural limitations. FlaUI was created as a complete rewrite to replace White. Only listed here because existing codebases may still reference it. Migrate to FlaUI for any new or maintained project.

### Snoop

- **Link:** https://github.com/snoopwpf/snoopwpf
- **What it does:** Open-source WPF spy/inspector utility. Browses the visual tree, logical tree, and automation tree of any running WPF app without a debugger. Allows live property editing, trigger inspection, and breakpoints on property changes.
- **Loop phase:** implement, verify (manual inspection)
- **Install:** Download from [GitHub Releases](https://github.com/snoopwpf/snoopwpf/releases) or install via Chocolatey/Scoop.
- **Claude Code integration:** Not directly invocable (GUI tool). Claude Code can remind developers to use Snoop for visual debugging when UI issues are detected.
- **Notes:** Tested with .NET 6, 7, 8, 9, and 10. Improved settings system in recent versions allows sharing settings across snooped applications. WPF-only -- does not support WinUI 3 (use UWPSpy instead).

### MVVM Unit Testing (pattern, not a tool)

- **What it does:** ViewModels in WPF/MAUI follow MVVM, making them testable without UI automation. Test commands, property changes (`INotifyPropertyChanged`), and service interactions using standard unit test frameworks.
- **Loop phase:** verify
- **Tools:**
  ```
  # Test frameworks
  dotnet add package xunit
  dotnet add package NUnit
  dotnet add package MSTest.TestFramework

  # Mocking
  dotnet add package NSubstitute    # Recommended for new projects (cleaner syntax)
  dotnet add package Moq             # Mature, widely used (SponsorLink concern noted)

  # Assertions
  dotnet add package FluentAssertions
  ```
- **Claude Code integration:** CLI shell-out via `dotnet test`. Claude Code generates ViewModel tests that verify command execution, property notification, and service calls without touching the UI layer.
- **Notes:** NSubstitute is the recommended default for new .NET projects in 2025-2026 for its readability and refactor-friendliness. Moq remains powerful but the SponsorLink telemetry controversy has driven migration. CommunityToolkit.Mvvm attributes (`[ObservableProperty]`, `[RelayCommand]`) generate boilerplate that is directly testable.

---

## MAUI Testing (verify)

### Appium for MAUI

- **Link:** https://learn.microsoft.com/en-us/dotnet/maui/deployment/unit-testing
- **What it does:** Microsoft's recommended approach for MAUI UI testing. Uses the Appium WebDriver protocol with platform-specific drivers (WinAppDriver on Windows, XCUITest on iOS, UIAutomator2 on Android) to automate MAUI apps across all targets.
- **Loop phase:** verify
- **Install:**
  ```
  # Appium server
  npm install -g appium

  # Platform drivers
  appium driver install windows
  appium driver install xcuitest
  appium driver install uiautomator2

  # Test project NuGet packages
  dotnet add package Appium.WebDriver
  dotnet add package NUnit           # Microsoft's MAUI samples use NUnit
  dotnet add package Plugin.Maui.UITestHelpers  # Migration helpers
  ```
- **Claude Code integration:** CLI shell-out. Start Appium, then `dotnet test`. BrowserStack App Automate integration available for cloud device testing.
- **Notes:** xUnit is the framework used internally by the MAUI team. NUnit is used in Microsoft's public samples. Both work. The `Plugin.Maui.UITestHelpers` package provides helpers extracted from the MAUI codebase to smooth the transition from Xamarin.UITest.

### DeviceRunners

- **Link:** https://github.com/mattleibow/DeviceRunners
- **What it does:** Runs unit tests directly on physical devices or emulators. Splits the UI from the test runner so tests execute in the context of a running MAUI app. Supports xUnit and NUnit.
- **Loop phase:** verify
- **Install:** Reference via NuGet; configure as a MAUI app that hosts the test runner.
- **Claude Code integration:** CLI shell-out. Build and deploy the test host app, then observe results. Primarily useful for testing platform-specific behavior that cannot be verified in a standard `dotnet test` environment.
- **Notes:** DeviceRunners works well for running unit tests on-device but is more complex to set up than Appium-based UI tests. Best for scenarios where you need to verify platform-specific APIs (sensors, file system, notifications) on real hardware.

### MAUI Unit Testing (ViewModel layer)

- **Link:** https://learn.microsoft.com/en-us/dotnet/maui/deployment/unit-testing
- **What it does:** Standard .NET unit tests targeting MAUI ViewModels, services, and converters. No MAUI runtime required -- tests run in a plain .NET test project.
- **Loop phase:** verify
- **Commands:**
  ```
  # Create a test project (not a MAUI project)
  dotnet new xunit -n MyApp.Tests
  dotnet add MyApp.Tests reference MyApp

  # Run tests
  dotnet test MyApp.Tests
  ```
- **Claude Code integration:** CLI shell-out. Claude Code generates ViewModel tests using CommunityToolkit.Mvvm patterns and runs them with `dotnet test`.
- **Notes:** Keep MAUI-specific types (pages, controls, platform services) behind interfaces so ViewModels can be tested without the MAUI runtime. Mock platform services with NSubstitute.

---

## Packaging & Certification (verify)

### MakeAppx.exe

- **Link:** https://learn.microsoft.com/en-us/windows/msix/package/create-app-package-with-makeappx-tool
- **What it does:** Creates MSIX/APPX packages and bundles from loose files. Also extracts, encrypts, and decrypts packages. Included in the Windows SDK.
- **Loop phase:** verify
- **Install:** Included with Windows SDK at `C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\makeappx.exe`
- **Commands:**
  ```
  # Create package from directory
  makeappx pack /d <input_directory> /p <output>.msix

  # Create bundle from packages
  makeappx bundle /d <input_directory> /p <output>.msixbundle

  # Extract package contents
  makeappx unpack /p <package>.msix /d <output_directory>
  ```
- **Claude Code integration:** CLI shell-out. Only `makeappx` (or tools wrapping it) can produce valid MSIX packages. Usually invoked automatically by `dotnet publish` but available directly for advanced scenarios.

### SignTool.exe

- **Link:** https://learn.microsoft.com/en-us/windows/msix/package/sign-app-package-using-signtool
- **What it does:** Digitally signs MSIX packages and executables. Required for MSIX installation -- unsigned packages cannot be installed.
- **Loop phase:** verify
- **Install:** Included with Windows SDK at `C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\signtool.exe`
- **Commands:**
  ```
  # Sign with a .pfx file
  signtool sign /fd SHA256 /a /f MyCert.pfx /p <password> MyApp.msix

  # Sign with an installed certificate
  signtool sign /fd SHA256 /n "My Certificate Name" MyApp.msix

  # Sign with timestamp (recommended for production)
  signtool sign /fd SHA256 /a /f MyCert.pfx /p <password> \
    /tr http://timestamp.digicert.com /td SHA256 MyApp.msix
  ```
- **Claude Code integration:** CLI shell-out. In CI, use Azure Key Vault for certificate storage and access signing credentials via pipeline variables. The `/fd SHA256` flag is required on Windows SDK builds 20236+.

### Windows App Certification Kit (WACK)

- **Link:** https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/windows-app-certification-kit
- **What it does:** Validates that an MSIX package meets Microsoft Store requirements. Tests security, performance, and API compliance. Required before Store submission.
- **Loop phase:** verify
- **Install:** Included with Windows SDK. The `appcert.exe` CLI is at the SDK bin path.
- **Commands:**
  ```
  # Validate an MSIX package
  appcert.exe test -appxpackagepath MyApp.msix -reportoutputpath report.xml

  # Run on a clean machine for best results (reboots during test = failure)
  ```
- **Claude Code integration:** CLI shell-out. Parse the XML report for pass/fail status. Best run on a clean Windows VM in CI.
- **Notes:** Run all WACK tests in a single session -- reboots or logoffs during testing are recorded as failures. A GitHub Action (`ChristopheLav/wack-certification`) wraps WACK for GitHub Actions pipelines.

### Microsoft Store Developer CLI (msstore)

- **Link:** https://github.com/microsoft/msstore-cli
- **What it does:** Cross-platform CLI (Windows, macOS, Linux) for publishing apps to the Microsoft Store. Configures projects, creates MSIX packages, and submits to Partner Center APIs.
- **Loop phase:** verify (submission)
- **Install:**
  ```
  # Install via .NET global tool
  dotnet tool install -g MSStore.CLI

  # Or from Microsoft Store
  # https://apps.microsoft.com/detail/9p53pc5s0phj
  ```
- **Commands:**
  ```
  # Configure Partner Center credentials
  msstore reconfigure --tenantId <id> --sellerId <id> --clientId <id>

  # Initialize project for Store
  msstore init

  # Package as MSIX
  msstore package

  # Publish to Store
  msstore publish

  # Check submission status
  msstore submission status
  ```
- **Claude Code integration:** CLI shell-out. Supports CI environments with service principal authentication. MFA will be required for Partner Center API access starting April 1, 2026.

---

## CI/CD Integration (verify)

### GitHub Actions (windows-latest)

- **Link:** https://github.com/jfversluis/MauiGithubActionsSample
- **What it does:** GitHub-hosted Windows runners include the .NET SDK, Windows SDK, and MSBuild. Builds WinUI, WPF, and MAUI Windows targets. The `windows-latest` image includes Visual Studio Build Tools.
- **Loop phase:** verify
- **Example workflow:**
  ```yaml
  name: Build Windows
  on: [push, pull_request]
  jobs:
    build:
      runs-on: windows-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-dotnet@v4
          with:
            dotnet-version: '10.0.x'
        - name: Install MAUI workload
          run: dotnet workload install maui
        - name: Build
          run: dotnet build src/MyApp/MyApp.csproj -f net10.0-windows10.0.19041.0 -c Release
        - name: Test
          run: dotnet test src/MyApp.Tests/MyApp.Tests.csproj -c Release
        - name: Publish MSIX
          run: dotnet publish src/MyApp/MyApp.csproj -f net10.0-windows10.0.19041.0 -c Release
  ```
- **Claude Code integration:** Claude Code generates and modifies workflow YAML files. Use `gh workflow run` and `gh run watch` to trigger and monitor builds.
- **Notes:** MAUI workload installation (`dotnet workload install maui`) adds ~2 minutes to CI. Cache NuGet packages with `actions/cache` to reduce restore time. For MSIX signing in CI, store the .pfx as a GitHub Secret and decode it in the pipeline.

### Azure DevOps Pipelines

- **Link:** https://learn.microsoft.com/en-us/windows/msix/desktop/cicd-overview
- **What it does:** Microsoft's CI/CD platform with deep MSIX integration. MSIX Packaging Extension available from the Visual Studio Marketplace. Supports Azure Key Vault for certificate management.
- **Loop phase:** verify
- **Key features:**
  - MSIX Packaging Extension automates build + package + sign
  - Azure Key Vault integration for secure certificate storage
  - Secure Files feature for .pfx certificates with password in Key Vault
  - YAML pipeline configuration with MSBuild tasks
- **Claude Code integration:** Claude Code can generate and edit `azure-pipelines.yml` files. Use the Azure CLI (`az pipelines run`) for triggering builds.
- **Notes:** For MSIX signing, never commit certificates to source control. Use Azure Key Vault or the Secure Files feature. The MSIX CI automation task from the Visual Studio Marketplace simplifies packaging in Azure Pipelines.

### WACK GitHub Action

- **Link:** https://github.com/ChristopheLav/wack-certification
- **What it does:** GitHub Action that runs the Windows App Certification Kit and generates test results as artifacts.
- **Loop phase:** verify
- **Usage:**
  ```yaml
  - uses: ChristopheLav/wack-certification@v1
    with:
      package-path: path/to/MyApp.msix
  ```
- **Claude Code integration:** Add to workflow YAML as a post-build step.

---

## Development & Diagnostic Tools (implement)

### XAML Hot Reload

- **Link:** https://learn.microsoft.com/en-us/visualstudio/xaml-tools/xaml-hot-reload
- **What it does:** Incrementally updates XAML UI in a running WPF, UWP, WinUI 3, or MAUI app without restarting. Starting in Visual Studio 2022 v17.14 Preview 2, also available at design-time (not just during debugging).
- **Loop phase:** implement
- **Claude Code integration:** Not directly invocable (Visual Studio feature). Claude Code edits XAML files; the developer sees changes reflected live if Hot Reload is active in their IDE.
- **Notes:** WinUI 3 Hot Reload has had stability issues historically (see microsoft-ui-xaml#7687). Generally reliable in current Windows App SDK releases but occasionally requires app restart.

### Live Visual Tree (Visual Studio)

- **Link:** https://learn.microsoft.com/en-us/visualstudio/xaml-tools/inspect-xaml-properties-while-debugging
- **What it does:** Built-in Visual Studio tool that displays the live visual tree of a running XAML app (WPF, UWP, WinUI 3, MAUI). Allows inspecting and editing properties in real time during debugging.
- **Loop phase:** implement
- **Claude Code integration:** Not directly invocable (Visual Studio debugger feature). Useful for developers to verify Claude Code's XAML changes visually.

### Snoop (WPF Inspector)

- **Link:** https://github.com/snoopwpf/snoopwpf
- **What it does:** Open-source WPF visual tree inspector. See [WPF Testing section](#snoop) above.
- **Loop phase:** implement
- **Notes:** WPF only. Does not require Visual Studio -- works as a standalone tool.

### UWPSpy (WinUI 3 Inspector)

- **Link:** https://github.com/m417z/UWPSpy
- **What it does:** Inspection tool for UWP and WinUI 3 applications. Views and manipulates UI elements and their properties in real time. Uses the XAML Diagnostic APIs (Windows 10 v1703+).
- **Loop phase:** implement
- **Install:** Download from [GitHub Releases](https://github.com/m417z/UWPSpy/releases). Run `UWPSpy.exe` and select the target app.
- **Claude Code integration:** Not directly invocable (GUI tool). Serves the same role as Snoop but for WinUI 3. Use Ctrl+D to identify elements.
- **Notes:** Windows 10 v1703+ required. The WinUI 3 equivalent of Snoop.

### WinUI3.Design.Diagnostics

- **Link:** https://github.com/KyleC69/WinUI3.Design.Diagnostics
- **What it does:** In-app diagnostics tool for WinUI 3 providing a live visual tree, style inspector, and resource lookup tracer. Embeds directly in your app.
- **Loop phase:** implement
- **Install:** Add as a NuGet package reference to your WinUI 3 project.
- **Hotkeys:** Ctrl+Alt+I (toggle inspector), Ctrl+Alt+P (picker), Alt+Shift+Click (select element).
- **Claude Code integration:** Claude Code adds the NuGet reference and diagnostic initialization code. The inspector runs inside the app, no external tool needed.
- **Notes:** Community project, MIT licensed. Early-stage but functional. Good for scenarios where UWPSpy cannot attach.

### Roslyn Analyzers & StyleCop

- **Link:** https://github.com/DotNetAnalyzers/StyleCopAnalyzers
- **What it does:** Static code analysis integrated into the build. Roslyn analyzers run during `dotnet build` and report diagnostics. StyleCop.Analyzers enforces C# style rules. Microsoft.CodeAnalysis.NetAnalyzers provides CA-prefixed quality rules.
- **Loop phase:** implement, verify
- **Install:**
  ```
  dotnet add package StyleCop.Analyzers
  dotnet add package Microsoft.CodeAnalysis.NetAnalyzers
  dotnet add package SonarAnalyzer.CSharp  # Optional, Sonar rules
  ```
- **Claude Code integration:** CLI shell-out. Analyzers run automatically during `dotnet build` and report warnings/errors. Claude Code reads diagnostics and applies fixes. `dotnet format analyzers` auto-fixes many violations.
- **Notes:** Configure severity levels in `.editorconfig`. Set `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` in the project file to enforce analyzer compliance in CI.

---

## Test Infrastructure (verify)

### dotnet test

- **Link:** https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test
- **What it does:** Runs unit and integration tests for xUnit, NUnit, MSTest, and TUnit projects. Supports two test platforms: VSTest (legacy) and Microsoft.Testing.Platform (MTP, modern).
- **Loop phase:** verify
- **Commands:**
  ```
  # Run all tests
  dotnet test

  # Run with code coverage (Coverlet)
  dotnet test --collect:"XPlat Code Coverage"

  # Run with .NET built-in coverage
  dotnet test --collect:"Code Coverage"

  # Filter tests
  dotnet test --filter "FullyQualifiedName~MyNamespace.MyTests"

  # Specific framework
  dotnet test -f net10.0
  ```
- **Claude Code integration:** CLI shell-out. Primary test command. Parse output for pass/fail counts and failure details.
- **Notes:** .NET 10 significantly improved `dotnet test` through Microsoft.Testing.Platform (MTP) integration, with better performance, diagnostics, and new capabilities. xUnit v3 uses MTP natively.

### Coverlet + ReportGenerator

- **Link:** https://github.com/coverlet-coverage/coverlet | https://github.com/danielpalme/ReportGenerator
- **What it does:** Coverlet collects code coverage data during test runs. ReportGenerator converts coverage XML into human-readable HTML reports.
- **Loop phase:** verify
- **Commands:**
  ```
  # Collect coverage
  dotnet test --collect:"XPlat Code Coverage"

  # Install ReportGenerator
  dotnet tool install -g dotnet-reportgenerator-globaltool

  # Generate HTML report
  reportgenerator \
    -reports:"**/TestResults/**/coverage.cobertura.xml" \
    -targetdir:"coverage-report" \
    -reporttypes:"Html;TextSummary"
  ```
- **Claude Code integration:** CLI shell-out. Run after `dotnet test` to generate coverage reports. The `TextSummary` report type outputs a plain-text summary Claude Code can parse directly for coverage percentages.
- **Notes:** Coverlet supports Cobertura, OpenCover, and lcov output formats. Set minimum thresholds in CI: ReportGenerator fails the build if coverage drops below configured minimums.

---

## Claude Code Integration (all phases)

### C# LSP Plugin

- **Link:** https://claude.com/plugins/csharp-lsp
- **What it does:** Enables IDE-like code intelligence in Claude Code for C# projects. Provides go-to-definition, find-references, hover type information, and real-time diagnostics. Finding all call sites takes ~50ms (vs ~45s with text search).
- **Loop phase:** plan, implement, verify
- **Install:**
  ```
  # Install the C# language server
  dotnet tool install --global csharp-ls

  # Install the Claude Code plugin
  claude plugin install csharp-lsp
  ```
- **Claude Code integration:** Plugin. Once installed, Claude Code's built-in LSP tool is enabled for C# files. Semantic understanding replaces text-based code search for navigation and refactoring.
- **Notes:** Requires .NET SDK 6.0+. The LSP provides 900x faster reference lookups compared to text search. Works with all C# project types including WinUI, WPF, and MAUI.

### csharp-lsp-mcp (C# + XAML MCP Server)

- **Link:** https://github.com/HYMMA/csharp-lsp-mcp
- **What it does:** MCP server providing C# and XAML language intelligence for Claude Code. Exposes IntelliSense, diagnostics, and code analysis through the Model Context Protocol. Supports both `.cs` and `.xaml` files.
- **Loop phase:** plan, implement, verify
- **Install:**
  ```
  git clone https://github.com/HYMMA/csharp-lsp-mcp.git
  cd csharp-lsp-mcp
  dotnet publish -c Release -o ./publish

  # Requires csharp-ls
  dotnet tool install --global csharp-ls
  ```
- **Key tools:** `csharp_set_workspace` (set solution directory), `csharp_diagnostics` (get compiler errors/warnings), hover info, completions.
- **Claude Code integration:** MCP server. Add to `.mcp.json` configuration. Provides XAML-aware intelligence that the standard C# LSP plugin does not cover.
- **Notes:** Particularly valuable for WinUI/WPF/MAUI development where XAML files need language intelligence alongside C#. Requires .NET SDK 6.0+ and the `csharp-ls` global tool.

### Claude Code LSP (Generic)

- **Link:** https://github.com/ktnyt/cclsp
- **What it does:** Non-IDE-dependent LSP integration for Claude Code. Supports 11 languages including C#. Provides go-to-definition, find-references, and diagnostics.
- **Loop phase:** plan, implement, verify
- **Claude Code integration:** Plugin. Alternative to the official C# LSP plugin for users who want a unified multi-language LSP setup.

---

## Sources

- [dotnet publish CLI for packaged MAUI apps](https://learn.microsoft.com/en-us/dotnet/maui/windows/deployment/publish-cli)
- [dotnet publish CLI for unpackaged MAUI apps](https://learn.microsoft.com/en-us/dotnet/maui/windows/deployment/publish-unpackaged-cli)
- [dotnet publish command reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-publish)
- [dotnet msbuild command reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-msbuild)
- [WinAppDriver GitHub](https://github.com/microsoft/WinAppDriver)
- [WinAppDriver alternatives (2026)](https://www.testsprite.com/use-cases/en/the-most-accurate-alternatives-to-winappdriver)
- [FlaUI GitHub](https://github.com/FlaUI/FlaUI)
- [Automating WPF with FlaUI and ReqnRoll](https://medium.com/@mail2sree6/automating-wpf-applications-with-flaui-and-reqnroll-in-c-bf6c637f32f2)
- [WPF UI testing demo (FlaUI)](https://github.com/MinimalWindowsDev/wpf-ui-testing-demo)
- [.NET MAUI UI testing with Appium](https://devblogs.microsoft.com/dotnet/dotnet-maui-ui-testing-appium/)
- [MAUI Appium NUnit sample](https://learn.microsoft.com/en-us/samples/dotnet/maui-samples/uitest-appium-nunit/)
- [DeviceRunners GitHub](https://github.com/mattleibow/DeviceRunners)
- [Plugin.Maui.UITestHelpers](https://github.com/jfversluis/Plugin.Maui.UITestHelpers)
- [BrowserStack + Appium + MAUI](https://devblogs.microsoft.com/dotnet/browserstack-appium-dotnet-maui/)
- [MakeAppx.exe reference](https://learn.microsoft.com/en-us/windows/msix/package/create-app-package-with-makeappx-tool)
- [SignTool MSIX signing](https://learn.microsoft.com/en-us/windows/msix/package/sign-app-package-using-signtool)
- [Windows App Certification Kit](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/windows-app-certification-kit)
- [WACK GitHub Action](https://github.com/ChristopheLav/wack-certification)
- [Microsoft Store Developer CLI](https://github.com/microsoft/msstore-cli)
- [MSIX CI/CD with Azure Key Vault](https://learn.microsoft.com/en-us/windows/msix/desktop/cicd-keyvault)
- [WinUI 3 CI setup](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/ci-for-winui3)
- [MAUI GitHub Actions sample](https://github.com/jfversluis/MauiGithubActionsSample)
- [MAUI libraries with GitHub Actions](https://devblogs.microsoft.com/dotnet/dotnet-maui-libraries-github-actions/)
- [XAML Hot Reload](https://learn.microsoft.com/en-us/visualstudio/xaml-tools/xaml-hot-reload)
- [Snoop WPF GitHub](https://github.com/snoopwpf/snoopwpf)
- [UWPSpy GitHub](https://github.com/m417z/UWPSpy)
- [WinUI3.Design.Diagnostics](https://github.com/KyleC69/WinUI3.Design.Diagnostics)
- [C# LSP Claude Plugin](https://claude.com/plugins/csharp-lsp)
- [csharp-lsp-mcp GitHub](https://github.com/HYMMA/csharp-lsp-mcp)
- [Claude Code LSP (cclsp)](https://github.com/ktnyt/cclsp)
- [dotnet test reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test)
- [Coverlet code coverage](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-code-coverage)
- [ReportGenerator GitHub](https://github.com/danielpalme/ReportGenerator)
- [StyleCop.Analyzers GitHub](https://github.com/DotNetAnalyzers/StyleCopAnalyzers)
- [Native AOT for MAUI](https://learn.microsoft.com/en-us/dotnet/maui/deployment/nativeaot)
- [TestStack.White (deprecated)](https://github.com/TestStack/White)
- [Moq vs NSubstitute (2025)](https://blog.dotnetconsult.tech/2025/12/moq-vs-nsubstitute-choosing-right.html)
- [Enhanced dotnet test with MTP](https://devblogs.microsoft.com/dotnet/dotnet-test-with-mtp/)
- [MAUI unit testing](https://learn.microsoft.com/en-us/dotnet/maui/deployment/unit-testing)
- [Create your first WinUI 3 app](https://learn.microsoft.com/en-us/windows/apps/winui/winui3/create-your-first-winui3-app)

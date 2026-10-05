---
id: 850594f9-e186-4361-a4b3-f0b2510ada9a
title: Xcode & Apple Build Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/apple/xcode-and-build
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Xcode & Apple Build Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Xcode & Apple Build Tools

**Date:** 2026-03-29
**Context:** Build system and Xcode CLI tools for Apple platform development with Claude Code.

---

## xcodebuild (implement/verify)

**What it is:** Apple's command-line tool for building, testing, analyzing, and archiving Xcode projects and workspaces. Ships with Xcode.

**Install:** Included with Xcode Command Line Tools (`xcode-select --install`).

### Common Commands

```bash
# Build a workspace scheme
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -configuration Debug build

# Build a project target
xcodebuild -project MyApp.xcodeproj -scheme MyApp -sdk iphonesimulator build

# Run tests
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro,OS=latest' \
  -resultBundlePath ./TestResults.xcresult

# Run tests on multiple destinations
xcodebuild test \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
  -destination 'platform=iOS Simulator,name=iPad Pro 13-inch (M4)'

# Archive for distribution
xcodebuild archive \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -archivePath ./build/MyApp.xcarchive

# Export an archive to IPA
xcodebuild -exportArchive \
  -archivePath ./build/MyApp.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath ./build/

# Clean build folder
xcodebuild clean -workspace MyApp.xcworkspace -scheme MyApp

# List available schemes
xcodebuild -list -workspace MyApp.xcworkspace

# List available destinations
xcodebuild -showdestinations -scheme MyApp

# Build for testing without running
xcodebuild build-for-testing \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro'

# Run previously built tests
xcodebuild test-without-building \
  -xctestrun MyApp.xctestrun \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro'
```

### Key Flags

| Flag | Purpose |
|------|---------|
| `-workspace` | Path to `.xcworkspace` |
| `-project` | Path to `.xcodeproj` (use when no workspace) |
| `-scheme` | Build scheme name |
| `-configuration` | `Debug` or `Release` |
| `-sdk` | Target SDK (`iphoneos`, `iphonesimulator`, `macosx`) |
| `-destination` | Device/simulator specifier (repeatable) |
| `-derivedDataPath` | Override DerivedData location |
| `-resultBundlePath` | Where to write `.xcresult` bundle |
| `-enableCodeCoverage YES` | Enable code coverage collection |
| `-parallel-testing-enabled YES` | Run tests in parallel |
| `-only-testing:` | Run specific test target/class/method |
| `-skip-testing:` | Skip specific tests |
| `-quiet` | Suppress stdout except warnings/errors |
| `ONLY_ACTIVE_ARCH=YES` | Build only for the active architecture (faster debug builds) |
| `CODE_SIGNING_ALLOWED=NO` | Disable code signing (useful in CI for test-only builds) |

### Output Formatters

Raw `xcodebuild` output is verbose and difficult to parse. Two formatters clean it up:

#### xcbeautify (recommended)

Written in Swift, compiles to a static binary. Default formatter in fastlane since v2.201.0.

```bash
# Install
brew install xcbeautify

# Usage (pipe xcodebuild output)
set -o pipefail && xcodebuild test -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
  2>&1 | xcbeautify

# With GitHub Actions renderer for annotations
set -o pipefail && xcodebuild build -scheme MyApp 2>&1 | xcbeautify --renderer github-actions
```

Features: colored output, supports parallel testing output, Swift Package Manager output, and Xcode's new build system.

- **Repo:** [cpisciotta/xcbeautify](https://github.com/cpisciotta/xcbeautify)

#### xcpretty (legacy)

Ruby-based formatter. Still works but slower and heavier dependency chain.

```bash
# Install
gem install xcpretty

# Usage
set -o pipefail && xcodebuild test -scheme MyApp 2>&1 | xcpretty

# Generate JUnit XML report
set -o pipefail && xcodebuild test -scheme MyApp 2>&1 | xcpretty -r junit
```

- **Repo:** [xcpretty/xcpretty](https://github.com/xcpretty/xcpretty)

### Claude Code Integration

Claude Code invokes `xcodebuild` directly via the Bash tool. Typical patterns:

- Build: `xcodebuild -workspace ... -scheme ... build 2>&1 | xcbeautify`
- Test: `xcodebuild test -scheme ... -destination ... -resultBundlePath ... 2>&1 | xcbeautify`
- Parse failures from the piped output or from the `.xcresult` bundle

---

## Simulator Management (implement/verify)

**What it is:** `xcrun simctl` is the CLI for creating, configuring, and controlling iOS/watchOS/tvOS/visionOS simulators.

**Install:** Included with Xcode.

### Device Lifecycle

```bash
# List all available runtimes and devices
xcrun simctl list
xcrun simctl list devices
xcrun simctl list runtimes
xcrun simctl list devicetypes

# Create a new simulator
xcrun simctl create "My Test Phone" "iPhone 16 Pro" "com.apple.CoreSimulator.SimRuntime.iOS-18-0"

# Boot / shutdown / erase
xcrun simctl boot <device-udid>
xcrun simctl shutdown <device-udid>
xcrun simctl erase <device-udid>

# Delete a simulator
xcrun simctl delete <device-udid>

# Delete all unavailable simulators
xcrun simctl delete unavailable
```

### App Management

```bash
# Install an app
xcrun simctl install booted /path/to/MyApp.app

# Launch an app
xcrun simctl launch booted com.example.MyApp

# Launch with stdout/stderr
xcrun simctl launch --console booted com.example.MyApp

# Terminate a running app
xcrun simctl terminate booted com.example.MyApp

# Uninstall an app
xcrun simctl uninstall booted com.example.MyApp

# Open a URL (deep link testing)
xcrun simctl openurl booted "myapp://deeplink/path"
```

### Screenshots & Video

```bash
# Take a screenshot
xcrun simctl io booted screenshot screenshot.png

# Record video (Ctrl+C to stop)
xcrun simctl io booted recordVideo recording.mp4
```

### Status Bar Override

Customize the simulator status bar for App Store screenshots:

```bash
# Full override for clean screenshots
xcrun simctl status_bar booted override \
  --time "9:41" \
  --dataNetwork "wifi" \
  --wifiMode active \
  --wifiBars 3 \
  --operatorName "" \
  --batteryState charged \
  --batteryLevel 100

# Show 5G indicator
xcrun simctl status_bar booted override --dataNetwork "5g"

# Clear overrides
xcrun simctl status_bar booted clear
```

### Push Notifications

```bash
# Send a push notification (requires .apns JSON file)
xcrun simctl push booted com.example.MyApp notification.apns

# notification.apns contents:
# {
#   "aps": {
#     "alert": { "title": "Test", "body": "Hello from simctl" },
#     "sound": "default"
#   }
# }

# Send via stdin
echo '{"aps":{"alert":"Test"}}' | xcrun simctl push booted com.example.MyApp -
```

### Other Useful Commands

```bash
# Add media (photos/videos) to simulator
xcrun simctl addmedia booted photo.jpg video.mp4

# Set device location
xcrun simctl location booted set 37.7749,-122.4194

# Get app container path
xcrun simctl get_app_container booted com.example.MyApp data

# Trigger iCloud sync
xcrun simctl icloud_sync booted

# Clone a device
xcrun simctl clone <source-udid> "Cloned Device"

# Pair Apple Watch with iPhone simulator
xcrun simctl pair <watch-udid> <phone-udid>

# Privacy permissions
xcrun simctl privacy booted grant photos com.example.MyApp
xcrun simctl privacy booted grant camera com.example.MyApp
xcrun simctl privacy booted reset all com.example.MyApp
```

### Claude Code Integration

Claude Code uses `xcrun simctl` via Bash for simulator management. The `booted` keyword targets the currently running simulator. For multiple simulators, use the UDID from `xcrun simctl list devices`.

---

## Result Bundle & Test Output (verify)

**What it is:** Tools for parsing `.xcresult` bundles produced by `xcodebuild` to extract test results, code coverage, screenshots, and logs.

### xcresulttool (built-in)

Ships with Xcode. Extracts structured data from `.xcresult` bundles.

```bash
# Get the root JSON object of a result bundle
xcrun xcresulttool get --path TestResults.xcresult --format json

# Get a specific object by ID
xcrun xcresulttool get --path TestResults.xcresult --id <ref-id> --format json

# Export an attachment (screenshot, etc.)
xcrun xcresulttool export --path TestResults.xcresult --id <ref-id> --output-path ./screenshot.png

# Get the test plan run summaries
xcrun xcresulttool get --path TestResults.xcresult --format json | \
  python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin), indent=2))"
```

- **Man page:** [xcresulttool(1)](https://keith.github.io/xcode-man-pages/xcresulttool.1.html)

### xccov (built-in)

Apple's code coverage CLI, included with Xcode.

```bash
# View human-readable coverage report
xcrun xccov view --report TestResults.xcresult

# Export coverage as JSON
xcrun xccov view --report --json TestResults.xcresult

# View coverage for a specific file
xcrun xccov view --file Sources/MyApp/ViewModel.swift --archive TestResults.xcresult

# Diff two coverage reports
xcrun xccov diff --json before.xcresult after.xcresult
```

To enable coverage collection: `xcodebuild test -enableCodeCoverage YES ...`

### xcparse

Open-source tool from ChargePoint for extracting data from `.xcresult` bundles.

```bash
# Install
brew install chargepoint/xcparse/xcparse

# Extract screenshots
xcparse screenshots TestResults.xcresult ./screenshots/

# Extract code coverage
xcparse codecov TestResults.xcresult ./coverage/

# Extract logs
xcparse logs TestResults.xcresult ./logs/
```

- **Repo:** [ChargePoint/xcparse](https://github.com/ChargePoint/xcparse)

### xcresultparser

Converts `.xcresult` files to multiple output formats (JUnit XML, Cobertura, HTML, Markdown).

```bash
# Install
brew install a7ex/formulae/xcresultparser

# Generate JUnit XML (for CI integration)
xcresultparser -o junit TestResults.xcresult > test-results.xml

# Generate Cobertura coverage XML
xcresultparser -o cobertura TestResults.xcresult > coverage.xml

# Generate HTML report
xcresultparser -o html TestResults.xcresult > report.html

# Generate Markdown summary
xcresultparser -o md TestResults.xcresult
```

- **Repo:** [a7ex/xcresultparser](https://github.com/a7ex/xcresultparser)

### XCLogParser

Parses Xcode's `.xcactivitylog` files (build and test logs) for build-time analysis.

```bash
# Install via SPM
git clone https://github.com/MobileNativeFoundation/XCLogParser.git
cd XCLogParser && swift build -c release

# Parse a log to JSON
xclogparser parse --project MyApp --reporter json

# Generate an HTML report
xclogparser parse --project MyApp --reporter html --output build_report.html

# Supported reporters: json, flatJson, summaryJson, chromeTracer, issues, html
```

Use cases: build-time analysis per module/file, tracking warnings/errors over time, Chrome Trace Viewer integration.

- **Repo:** [MobileNativeFoundation/XCLogParser](https://github.com/MobileNativeFoundation/XCLogParser)

### Claude Code Integration

Claude Code can invoke `xcrun xcresulttool` and `xcrun xccov` directly to inspect test results and coverage after running tests. For CI pipelines, `xcresultparser` provides JUnit and Cobertura output that integrates with standard reporting tools.

---

## Fastlane (implement/verify)

**What it is:** Ruby-based automation toolchain for building, testing, and releasing iOS and Android apps.

**Install:**

```bash
# Via Bundler (recommended)
gem install bundler
bundle init
# Add to Gemfile: gem "fastlane"
bundle install

# Or via Homebrew
brew install fastlane

# Initialize in project
fastlane init
```

### Fastfile Structure

```ruby
# fastlane/Fastfile

default_platform(:ios)

platform :ios do
  desc "Run tests"
  lane :test do
    scan(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      devices: ["iPhone 16 Pro"],
      code_coverage: true,
      result_bundle: true
    )
  end

  desc "Build for App Store"
  lane :release do
    build_app(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      export_method: "app-store",
      output_directory: "./build"
    )
  end

  desc "Upload to App Store Connect"
  lane :deploy do
    deliver(
      skip_screenshots: true,
      skip_metadata: false,
      force: true
    )
  end

  desc "Generate screenshots"
  lane :screenshots do
    snapshot(
      devices: ["iPhone 16 Pro", "iPad Pro 13-inch (M4)"],
      languages: ["en-US", "de-DE"],
      clear_previous_screenshots: true
    )
    frameit(white: true)  # Add device frames
  end
end
```

### Key Actions

| Action | Purpose | Alias |
|--------|---------|-------|
| `scan` | Run tests | `run_tests` |
| `build_app` | Compile and package | `gym`, `build_ios_app` |
| `deliver` | Upload to App Store Connect | `upload_to_app_store` |
| `snapshot` | Generate localized screenshots | `capture_screenshots` |
| `frameit` | Add device frames to screenshots | -- |
| `match` | Manage code signing for teams | `sync_code_signing` |
| `pilot` | Upload to TestFlight | `upload_to_testflight` |
| `cert` | Manage signing certificates | `get_certificates` |
| `sigh` | Manage provisioning profiles | `get_provisioning_profile` |
| `produce` | Create new app on App Store Connect | `create_app_online` |
| `pem` | Manage push notification certificates | `get_push_certificate` |
| `precheck` | Check app metadata before submission | `check_app_store_metadata` |

### match (Team Code Signing)

Shares one code signing identity across the team using encrypted storage.

```ruby
# Fastfile lane
lane :certificates do
  match(
    type: "appstore",         # or "development", "adhoc", "enterprise"
    app_identifier: "com.example.MyApp",
    git_url: "https://github.com/org/certificates.git",  # or S3/GCS
    readonly: true            # don't create new certs, just fetch
  )
end
```

Storage options: Git repo (encrypted), Google Cloud Storage, Amazon S3.

### Claude Code Integration

Claude Code can invoke `fastlane <lane>` or `bundle exec fastlane <lane>` via Bash. Fastlane is most useful for multi-step workflows (build + sign + upload) and team code signing via match.

---

## Code Signing (implement)

**What it is:** CLI tools for managing certificates, provisioning profiles, and signing Apple binaries.

### Finding Identities

```bash
# List all valid code signing identities
security find-identity -v -p codesigning

# Sample output:
# 1) ABC123... "Apple Development: name@example.com (TEAMID)"
# 2) DEF456... "Apple Distribution: Company Name (TEAMID)"
```

### Signing Binaries

```bash
# Sign an app
codesign -s "Apple Development: name@example.com (TEAMID)" MyApp.app

# Sign with entitlements
codesign -s "Apple Distribution: Company Name" \
  --entitlements MyApp.entitlements \
  MyApp.app

# Force re-sign (replace existing signature)
codesign -f -s "Apple Development: ..." MyApp.app

# Deep sign (sign all nested code)
codesign --deep -s "Apple Development: ..." MyApp.app
```

### Verification

```bash
# Verify a signature
codesign -v --verbose MyApp.app

# Display signing info
codesign -d -v MyApp.app

# Display entitlements
codesign -d --entitlements - MyApp.app

# Verify against Gatekeeper policy
spctl --assess --verbose MyApp.app
```

### Provisioning Profiles

```bash
# View profile contents
security cms -D -i profile.mobileprovision

# Installed profiles location
ls ~/Library/MobileDevice/Provisioning\ Profiles/

# Decode a profile to readable plist
security cms -D -i profile.mobileprovision | plutil -convert xml1 -o - -
```

### Automatic Signing in xcodebuild

```bash
# Let Xcode manage signing automatically
xcodebuild build \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -allowProvisioningUpdates

# Disable signing (for CI test-only builds)
xcodebuild test \
  -scheme MyApp \
  CODE_SIGNING_ALLOWED=NO \
  CODE_SIGN_IDENTITY="" \
  PROVISIONING_PROFILE=""
```

### Claude Code Integration

Claude Code uses `security find-identity` to discover available signing identities and `codesign` for signing operations. For CI workflows, fastlane match or manual certificate management is preferred over interactive signing.

---

## Build Caching & Performance (implement)

### Xcode Compilation Cache (Xcode 26+)

Apple's built-in compilation cache, opt-in as of Xcode 26.

```bash
# Enable via build setting
xcodebuild build \
  -scheme MyApp \
  COMPILATION_CACHE_ENABLE_CACHING=YES

# Or set in Xcode: Build Settings > Compilation Cache > Enable Caching = YES
```

Limitations: many tasks not yet cacheable (build graph computation, some Swift package compilations). Cross-machine reuse limited by absolute path dependencies.

### ccache (C/C++/Objective-C)

Compiler cache for C-family languages. Does not support Swift.

```bash
# Install
brew install ccache

# Configure for Xcode (set CC in build settings)
# In xcconfig or build settings:
# CC = /opt/homebrew/bin/ccache clang
# CXX = /opt/homebrew/bin/ccache clang++

# View cache stats
ccache -s

# Clear cache
ccache -C
```

Best for: projects with significant Objective-C/C/C++ code, CocoaPods with C dependencies, mixed-language projects.

- **Site:** [ccache.dev](https://ccache.dev/)

### XCRemoteCache (Spotify)

Remote build cache that shares artifacts between CI and developer machines. Cut Spotify's clean build times by 70%.

```bash
# Install
brew install xcremotecache

# Two modes:
# - Producer (CI): generates and uploads artifacts
# - Consumer (dev machines): downloads cached artifacts

# Setup requires .rcinfo configuration file and HTTP server (S3, GCS, etc.)
```

Supports Objective-C, Swift, and mixed targets. Works with CocoaPods and Carthage projects.

- **Repo:** [spotify/XCRemoteCache](https://github.com/spotify/XCRemoteCache)

### SwiftPM Dependency Caching

```bash
# Dependencies resolve to Package.resolved
# Default cache location: ~/Library/Developer/Xcode/DerivedData

# Specify custom derived data path
xcodebuild build -derivedDataPath ./DerivedData -scheme MyApp

# In CI, cache these paths between builds:
# - .build/ (for SPM CLI projects)
# - DerivedData/<project>/SourcePackages/
# - ~/Library/Developer/Xcode/DerivedData/<project>/SourcePackages/
```

### Xcode Cache GitHub Action

Caches Xcode's DerivedData for incremental CI builds.

```yaml
# .github/workflows/build.yml
- uses: irgaly/xcode-cache@v1
  with:
    key: xcode-cache-${{ hashFiles('**/*.swift') }}
    restore-keys: xcode-cache-
```

- **Repo:** [irgaly/xcode-cache](https://github.com/irgaly/xcode-cache)

### Claude Code Integration

Claude Code can enable `COMPILATION_CACHE_ENABLE_CACHING=YES` in xcodebuild invocations. For ccache, Claude Code can verify it is installed and configured in the project's build settings. Cache path management (DerivedData, SPM packages) is done via standard file operations.

---

## CI/CD Integration (verify)

### Xcode Cloud

Apple's built-in CI/CD, integrated directly into Xcode.

| Feature | Detail |
|---------|--------|
| **Pricing** | 25 free compute hours/month with Apple Developer Program; paid tiers at 100/250/1000 hours ($49.95-$399.99/month) |
| **Triggers** | Push, PR, tag, schedule |
| **Platforms** | iOS, macOS, watchOS, tvOS, visionOS |
| **Code signing** | Automatic, managed by Apple |
| **Limitations** | Apple-only, no text-based config files, workflows configured in Xcode GUI or App Store Connect |
| **Custom scripts** | `ci_scripts/ci_post_clone.sh`, `ci_scripts/ci_pre_xcodebuild.sh`, `ci_scripts/ci_post_xcodebuild.sh` |

- **Docs:** [developer.apple.com/xcode-cloud](https://developer.apple.com/xcode-cloud/)

### GitHub Actions

```yaml
# .github/workflows/ios.yml
name: iOS CI
on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: macos-15  # Apple Silicon M1, 3-core, 7GB RAM
    steps:
      - uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_16.app

      - name: Build
        run: |
          set -o pipefail
          xcodebuild build \
            -workspace MyApp.xcworkspace \
            -scheme MyApp \
            -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
            ONLY_ACTIVE_ARCH=YES \
            2>&1 | xcbeautify --renderer github-actions

      - name: Test
        run: |
          set -o pipefail
          xcodebuild test \
            -workspace MyApp.xcworkspace \
            -scheme MyApp \
            -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
            -resultBundlePath TestResults.xcresult \
            -enableCodeCoverage YES \
            2>&1 | xcbeautify --renderer github-actions
```

Runner specs: `macos-15` provides Apple M1, 3-core CPU, 7GB RAM with pre-installed Xcode versions.

### Codemagic

Pay-as-you-go, Apple Silicon runners, ~40% faster than Bitrise in benchmarks.

```yaml
# codemagic.yaml
workflows:
  ios-workflow:
    name: iOS Build & Test
    instance_type: mac_mini_m2
    environment:
      xcode: latest
    scripts:
      - name: Run tests
        script: |
          xcodebuild test \
            -workspace MyApp.xcworkspace \
            -scheme MyApp \
            -destination 'platform=iOS Simulator,name=iPhone 16 Pro'
```

- **Site:** [codemagic.io](https://codemagic.io/)

### Bitrise

Mobile-focused CI/CD with Apple Silicon runners up to M4 Pro. New Xcode versions available within 24 hours of Apple release.

- **Site:** [bitrise.io](https://bitrise.io/)

### Claude Code Integration

Claude Code can generate and edit CI configuration files (`.github/workflows/*.yml`, `codemagic.yaml`, Xcode Cloud `ci_scripts/`). It can also trigger GitHub Actions runs via `gh workflow run` and check status with `gh run list`.

---

## Alternative Build Systems (implement)

### Bazel (rules_apple + rules_swift)

Google's build system with Apple platform support via community-maintained rules.

```bash
# Install
brew install bazelisk  # version manager for Bazel

# Example BUILD file
# load("@rules_apple//apple:ios.bzl", "ios_application")
# load("@rules_swift//swift:swift.bzl", "swift_library")
#
# swift_library(
#     name = "Sources",
#     srcs = glob(["Sources/**/*.swift"]),
# )
#
# ios_application(
#     name = "MyApp",
#     bundle_id = "com.example.MyApp",
#     minimum_os_version = "17.0",
#     deps = [":Sources"],
# )

# Build
bazel build //MyApp

# Test
bazel test //MyAppTests

# Generate Xcode project (via rules_xcodeproj)
bazel run //:xcodeproj
```

Advantages: hermetic builds, remote caching, remote execution, fine-grained parallelism. Disadvantages: steep learning curve, Starlark configuration language, complex setup.

- **Repo:** [bazelbuild/rules_apple](https://github.com/bazelbuild/rules_apple)
- **Repo:** [bazelbuild/rules_swift](https://github.com/bazelbuild/rules_swift)
- **Docs:** [bazel.build/docs/bazel-and-apple](https://bazel.build/docs/bazel-and-apple)

### Buck2 (Meta)

Meta's Rust-based build system, successor to Buck1. 2x faster than Buck1 in internal benchmarks.

```bash
# Install (requires Rust toolchain)
# See https://buck2.build/docs/getting_started/

# Apple iOS rules available:
# apple_bundle() - build app bundles with signing
# apple_library() - build static/dynamic libraries
# apple_test() - run XCTest bundles

# Build
buck2 build //MyApp:MyApp

# Test
buck2 test //MyApp:MyAppTests
```

Configuration: Starlark-based (like Bazel). Supports remote execution and caching. Used at scale by Meta for iOS.

- **Site:** [buck2.build](https://buck2.build/)
- **Repo:** [facebook/buck2](https://github.com/facebook/buck2)

### Tuist

Project generation and build management tool that uses Swift for configuration.

```bash
# Install
brew install tuist

# Initialize a new project
tuist init --platform ios

# Generate Xcode project from manifests
tuist generate

# Build
tuist build MyApp

# Test (with selective testing based on changes)
tuist test MyApp

# Cache dependencies as pre-built binaries
tuist cache warm

# Edit project manifests in Xcode
tuist edit

# Visualize dependency graph
tuist graph
```

Configuration uses `Project.swift` and `Workspace.swift` (Swift DSL, with Xcode autocompletion). As of 2026, Tuist supports cross-platform (Linux CLI for server commands), Gradle cache integration, and flaky test detection.

- **Site:** [tuist.dev](https://tuist.dev/)
- **Docs:** [docs.tuist.dev](https://docs.tuist.dev/)

### Claude Code Integration

Claude Code can read/write Bazel BUILD files, Buck2 BUCK files, and Tuist `Project.swift` manifests. For Tuist, Claude Code can run `tuist generate` to produce Xcode projects and `tuist build`/`tuist test` for builds. Bazel and Buck2 are invoked via their respective CLIs through Bash.

---

## Claude Code Integration (all phases)

### MCP Servers

Model Context Protocol servers give Claude Code structured, tool-based access to Xcode and simulator functionality instead of raw shell output parsing.

#### XcodeBuildMCP (Sentry)

The most comprehensive Xcode MCP server. 59 tools covering builds, tests, simulators, real device deployment, and LLDB debugging.

```bash
# Install via Homebrew
brew tap getsentry/xcodebuildmcp
brew install xcodebuildmcp

# Or via npx
npx -y xcodebuildmcp@latest mcp

# Configure in .mcp.json
# {
#   "mcpServers": {
#     "xcodebuild": {
#       "command": "xcodebuildmcp",
#       "args": ["mcp"]
#     }
#   }
# }
```

Capabilities: build projects, run tests, manage simulators, deploy to real devices, LLDB debugging -- all without Xcode running. Returns structured JSON instead of raw logs.

- **Site:** [xcodebuildmcp.com](https://www.xcodebuildmcp.com/)
- **Repo:** [getsentry/XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP)

#### SwiftLens

MCP server for deep semantic analysis of Swift codebases via SourceKit-LSP. Provides compiler-grade code understanding to AI agents.

```bash
# Install (requires Swift toolchain)
# Configure in .mcp.json for Claude Code

# Capabilities:
# - Go to definition, find references, symbol search
# - Type information, documentation lookup
# - Diagnostics and semantic analysis
```

Works with Claude Desktop, Claude Code, Cursor, and other MCP clients. Model-agnostic.

- **Repo:** [swiftlens/swiftlens](https://github.com/swiftlens/swiftlens)
- **Site:** [swiftlens.tools](https://swiftlens.tools/)

#### iOS Simulator MCP Servers

Several MCP servers provide simulator control:

| Server | Capabilities |
|--------|-------------|
| [ios-simulator-mcp](https://github.com/joshuayoes/ios-simulator-mcp) | Screenshots, UI hierarchy, tap, swipe, type, GPS |
| [simctl-mcp-server](https://github.com/nzrsky/simctl-mcp-server) | Structured xcrun simctl access |
| [whitesmith/ios-simulator-mcp](https://github.com/whitesmith/ios-simulator-mcp) | Screenshots, UI hierarchy, gestures |
| [InditexTech/mcp-server-simulator-ios-idb](https://github.com/InditexTech/mcp-server-simulator-ios-idb) | IDB-based simulator interaction |

#### Xcode MCP (devyhan)

General-purpose Xcode MCP server: project management, building, testing, archiving, code signing, simulator management, real device deployment.

- **Repo:** [devyhan/xcode-mcp](https://mcpservers.org/servers/devyhan/xcode-mcp)

### Swift LSP Plugin

Claude Code's official Swift LSP plugin integrates SourceKit-LSP for code intelligence.

```bash
# Plugin: swift-lsp (from claude-plugins-official)
# Provides: go-to-definition, find-references, hover info, diagnostics
# Requires: Swift toolchain installed (ships with Xcode)
```

Works with Swift Package Manager projects. Supports cross-language navigation for Swift and C-based languages.

- **Plugin page:** [claude.com/plugins/swift-lsp](https://claude.com/plugins/swift-lsp)

### cclsp (Generic LSP Bridge)

Generic MCP server that bridges any LSP server (including sourcekit-lsp) to Claude Code.

```bash
# Install
# See https://github.com/ktnyt/cclsp

# Supports sourcekit-lsp among other language servers
```

- **Repo:** [ktnyt/cclsp](https://github.com/ktnyt/cclsp)

### Direct CLI Access

Without MCP servers, Claude Code invokes all Apple tools directly through Bash:

| Tool | Phase | Example |
|------|-------|---------|
| `xcodebuild` | implement, verify | `xcodebuild build -scheme MyApp` |
| `xcrun simctl` | implement, verify | `xcrun simctl boot <udid>` |
| `xcrun xcresulttool` | verify | `xcrun xcresulttool get --path Results.xcresult` |
| `xcrun xccov` | verify | `xcrun xccov view --report --json Results.xcresult` |
| `swift build` | implement | `swift build` (SPM projects) |
| `swift test` | verify | `swift test --parallel` |
| `swift package` | implement | `swift package resolve` |
| `codesign` | implement | `codesign -s "Identity" App.app` |
| `security` | implement | `security find-identity -v -p codesigning` |
| `fastlane` | implement, verify | `bundle exec fastlane test` |
| `tuist` | implement | `tuist generate` |
| `bazel` | implement, verify | `bazel build //MyApp` |

### Recommended Setup

For the best Claude Code experience with Apple development:

1. **XcodeBuildMCP** -- structured build/test/simulator access (install via Homebrew)
2. **Swift LSP plugin** -- code intelligence for Swift files (install from Claude plugins)
3. **xcbeautify** -- readable build output when using xcodebuild directly (install via Homebrew)
4. **SwiftLens** (optional) -- deep semantic Swift analysis beyond basic LSP

---

## Sources

- [xcodebuild man page](https://keith.github.io/xcode-man-pages/xcodebuild.1.html)
- [xcodebuild CLI cheat sheet (Dan Fabulich)](https://danfabulich.medium.com/xcodebuild-cli-cheat-sheet-b7ee7b3d5fc6)
- [Building from the Command Line - Apple TN2339](https://developer.apple.com/library/archive/technotes/tn2339/_index.html)
- [How to build iOS apps from the command line (Tricentis)](https://www.tricentis.com/learn/xcodebuild-ios-command-line-ci-cd)
- [simctl - NSHipster](https://nshipster.com/simctl/)
- [xcrun simctl reference (iOS Dev Recipes)](https://www.iosdev.recipes/simctl/)
- [simctl: Control iOS Simulators (XCBlog)](https://medium.com/xcblog/simctl-control-ios-simulators-from-command-line-78b9006a20dc)
- [xcresulttool man page](https://keith.github.io/xcode-man-pages/xcresulttool.1.html)
- [ChargePoint/xcparse](https://github.com/ChargePoint/xcparse)
- [a7ex/xcresultparser](https://github.com/a7ex/xcresultparser)
- [MobileNativeFoundation/XCLogParser](https://github.com/MobileNativeFoundation/XCLogParser)
- [xccov: Xcode Code Coverage Report for Humans](https://medium.com/xcblog/xccov-xcode-code-coverage-report-for-humans-466a4865aa18)
- [fastlane docs](https://docs.fastlane.tools/)
- [fastlane scan docs](https://docs.fastlane.tools/actions/scan/)
- [fastlane build_ios_app docs](https://docs.fastlane.tools/actions/build_ios_app/)
- [fastlane match docs](https://docs.fastlane.tools/actions/match/)
- [Inside Code Signing (objc.io)](https://www.objc.io/issues/17-security/inside-code-signing/)
- [TN3125: Inside Code Signing - Provisioning Profiles (Apple)](https://developer.apple.com/documentation/technotes/tn3125-inside-code-signing-provisioning-profiles)
- [codesigning.guide](https://codesigning.guide/)
- [ccache.dev](https://ccache.dev/)
- [spotify/XCRemoteCache](https://github.com/spotify/XCRemoteCache)
- [Introducing XCRemoteCache (Spotify Engineering)](https://engineering.atspotify.com/2021/11/introducing-xcremotecache-the-ios-remote-caching-tool-that-cut-our-clean-build-times-by-70)
- [irgaly/xcode-cache GitHub Action](https://github.com/irgaly/xcode-cache)
- [Tuist Xcode Cache](https://docs.tuist.dev/en/guides/features/cache/xcode-cache)
- [10x faster Xcode CI builds with slot caching](https://jeffverkoeyen.com/blog/2025/12/15/SlotWarmedCaching/)
- [Xcode Cloud Overview (Apple)](https://developer.apple.com/xcode-cloud/)
- [GitHub CI/CD vs. Xcode Cloud (Velotio)](https://www.velotio.com/engineering-blog/github-ci-cd-vs-xcode-cloud-a-comprehensive-comparison-for-ios-platform)
- [CI/CD Build Speed Benchmark (Codemagic)](https://blog.codemagic.io/build-speed-benchmark-comparison/)
- [Bitrise vs GitHub Actions](https://bitrise.io/resources/compare/bitrise-vs-github)
- [bazelbuild/rules_apple](https://github.com/bazelbuild/rules_apple)
- [bazelbuild/rules_swift](https://github.com/bazelbuild/rules_swift)
- [Bazel and Apple (bazel.build)](https://bazel.build/docs/bazel-and-apple)
- [Buck2 (buck2.build)](https://buck2.build/)
- [facebook/buck2](https://github.com/facebook/buck2)
- [Tuist docs](https://docs.tuist.dev/)
- [getsentry/XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP)
- [XcodeBuildMCP site](https://www.xcodebuildmcp.com/)
- [Two MCP Servers Made Claude Code an iOS Build System](https://blakecrosley.com/blog/xcode-mcp-claude-code)
- [swiftlens/swiftlens](https://github.com/swiftlens/swiftlens)
- [Swift LSP Claude Plugin](https://claude.com/plugins/swift-lsp)
- [ktnyt/cclsp](https://github.com/ktnyt/cclsp)
- [cpisciotta/xcbeautify](https://github.com/cpisciotta/xcbeautify)
- [xcpretty/xcpretty](https://github.com/xcpretty/xcpretty)
- [joshuayoes/ios-simulator-mcp](https://github.com/joshuayoes/ios-simulator-mcp)
- [nzrsky/simctl-mcp-server](https://github.com/nzrsky/simctl-mcp-server)
- [nicklockwood/SwiftFormat](https://github.com/nicklockwood/SwiftFormat)
- [swiftlang/swift-format](https://github.com/swiftlang/swift-format)
- [Xcodebuild Formatters (fastlane docs)](https://docs.fastlane.tools/best-practices/xcodebuild-formatters/)
- [Overriding status bar settings (Jesse Squires)](https://www.jessesquires.com/blog/2019/09/26/overriding-status-bar-settings-ios-simulator/)
- [Claude Code iOS dev guide (keskinonur)](https://github.com/keskinonur/claude-code-ios-dev-guide)

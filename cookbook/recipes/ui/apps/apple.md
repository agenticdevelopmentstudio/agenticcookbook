---
id: c5778e2d-2f3b-4cbd-809b-39ed4b57ff57
title: "Apple Test App Suite"
domain: agenticdevelopercookbook://recipes/ui/apps/apple
type: recipe
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-03-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "XcodeGen-generated test app suite with component catalog targets for all five Apple platforms"
platforms:
  - ios
  - macos
  - swift
  - typescript
tags:
  - apple
  - apps
  - ui
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# Apple Test App Suite

## Overview

An XcodeGen-generated Xcode project with app targets for all five Apple platforms. Each app displays a component catalog — a navigable list of every UI component implemented from `ui/` specs, showing all states for visual testing and snapshot verification.

## Terminology

| Term | Definition |
|------|-----------|
| Catalog | A navigable list of all implemented components, each showing every state from its spec |
| Catalog entry | A single view showing one component in all its states |
| TestSharedKit | Local SPM package containing code shared across all five platform targets |

## Behavioral Requirements

### Project structure

- **xcodegen-project**: The project MUST be generated using XcodeGen from a `project.yml` file.
- **output-directory**: The generated project MUST be output to `Tests/Projects/Apple/`.
- **five-platform-targets**: The project MUST contain five app targets, one per Apple platform:

  | Target | Platform | Deployment Target | Bundle ID |
  |--------|----------|-------------------|-----------|
  | LitterboxTestiOS | iOS | 17.0 | com.litterbox.test.ios |
  | LitterboxTestMac | macOS | 14.0 | com.litterbox.test.mac |
  | LitterboxTestWatch | watchOS | 10.0 | com.litterbox.test.watch |
  | LitterboxTestTV | tvOS | 17.0 | com.litterbox.test.tv |
  | LitterboxTestVision | visionOS | 1.0 | com.litterbox.test.vision |

- **standalone-swiftui-apps**: Each target MUST be a standalone SwiftUI app. watchOS MUST use independent app mode (no WatchKit companion).
- **test-shared-kit-package**: A local Swift package `TestSharedKit` MUST exist at `Tests/Projects/Apple/TestSharedKit/` and MUST target all five platforms at the deployment versions in five-platform-targets.
- **depend-on-shared-kit**: All five app targets MUST depend on `TestSharedKit`.

### Source layout

- **per-platform-source-dir**: Each target MUST have its own source directory under `Sources/{platform}/` containing the app entry point.
- **shared-source-directory**: A `Shared/` directory MUST be added as a source directory to all targets. It contains:
  - `Shared/Components/` — component implementations from `ui/` specs
  - `Shared/Catalog/` — catalog views showing all states per component
- **os-compilation-conditions**: Platform-specific adaptations within shared code MUST use `#if os(...)` compilation conditions.

### Catalog behavior

- **catalog-root-view**: Each app's entry point MUST display a `ComponentCatalogView` as its root view.
- **adaptive-navigation**: `ComponentCatalogView` MUST use `NavigationSplitView` on macOS, iPadOS, and visionOS, and `NavigationStack` on iPhone, watchOS, and tvOS.
- **navigable-component-list**: The catalog MUST list all implemented components by name. Selecting a component MUST navigate to its catalog entry view.
- **all-states-per-component**: Each catalog entry view MUST display the component in every state defined in its spec (default, pressed, disabled, focused, loading, etc.), each in its own labeled section.
- **preview-per-entry**: Each catalog entry view MUST include a `#Preview` block.

### Adding a component

- **adding-component-steps**: When adding a new component, the implementer MUST:
  1. Read the component spec from `ui/`
  2. Implement the component in `Shared/Components/`
  3. Create a catalog entry view in `Shared/Catalog/` showing all states
  4. Register the entry in `ComponentCatalogView`
  5. Build all five targets to verify cross-platform compatibility

## Data Structures

### project.yml

```yaml
name: LitterboxTests
settings:
  base:
    GENERATE_INFOPLIST_FILE: YES
options:
  bundleIdPrefix: com.litterbox.test
  deploymentTarget:
    iOS: "17.0"
    macOS: "14.0"
    watchOS: "10.0"
    tvOS: "17.0"
    visionOS: "1.0"
packages:
  TestSharedKit:
    path: TestSharedKit
targets:
  LitterboxTestiOS:
    type: application
    platform: iOS
    sources:
      - Sources/iOS
      - Shared
    dependencies:
      - package: TestSharedKit
  LitterboxTestMac:
    type: application
    platform: macOS
    sources:
      - Sources/macOS
      - Shared
    dependencies:
      - package: TestSharedKit
  LitterboxTestWatch:
    type: application
    platform: watchOS
    sources:
      - Sources/watchOS
      - Shared
    dependencies:
      - package: TestSharedKit
  LitterboxTestTV:
    type: application
    platform: tvOS
    sources:
      - Sources/tvOS
      - Shared
    dependencies:
      - package: TestSharedKit
  LitterboxTestVision:
    type: application
    platform: visionOS
    sources:
      - Sources/visionOS
      - Shared
    dependencies:
      - package: TestSharedKit
```

### Source file layout

```
Tests/Projects/Apple/
├── project.yml
├── TestSharedKit/
│   ├── Package.swift
│   └── Sources/
│       └── TestSharedKit/
│           └── ComponentCatalog.swift
├── Sources/
│   ├── iOS/
│   │   └── LitterboxTestiOSApp.swift
│   ├── macOS/
│   │   └── LitterboxTestMacApp.swift
│   ├── watchOS/
│   │   └── LitterboxTestWatchApp.swift
│   ├── tvOS/
│   │   └── LitterboxTestTVApp.swift
│   └── visionOS/
│       └── LitterboxTestVisionApp.swift
└── Shared/
    ├── Components/          ← component implementations from ui/ specs
    └── Catalog/             ← catalog entry views showing all states
```

### Catalog entry pattern

```swift
struct PrimaryButtonCatalog: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                Text("PrimaryButton").font(.title)

                Section("Default") {
                    PrimaryButton("Label", action: {})
                }
                Section("Disabled") {
                    PrimaryButton("Label", action: {}).disabled(true)
                }
                Section("Loading") {
                    PrimaryButton("Label", isLoading: true, action: {})
                }
            }
            .padding()
        }
    }
}

#Preview {
    PrimaryButtonCatalog()
}
```

## Appearance

Not applicable — this recipe defines app-level structure and build configuration. Visual appearance is defined by window and component recipes.

## States

Not applicable — app-level states (launching, active, background, terminated) are defined by the platform, not this recipe. See `recipes/app/lifecycle.md` for app state management.

## Accessibility

Not applicable — this recipe defines project structure and build configuration. Accessibility requirements are defined per-component in the UI recipes.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| apple-001 | xcodegen-project | Run `xcodegen generate` in project dir | `LitterboxTests.xcodeproj` is created |
| apple-002 | five-platform-targets | Open generated project | 5 app targets exist with correct names and platforms |
| apple-003 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestiOS | Build succeeds, app launches with catalog |
| apple-004 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestMac | Build succeeds, app launches with catalog |
| apple-005 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestWatch | Build succeeds, app launches with catalog |
| apple-006 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestTV | Build succeeds, app launches with catalog |
| apple-007 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestVision | Build succeeds, app launches with catalog |
| apple-008 | adaptive-navigation | Run LitterboxTestMac | Root view is NavigationSplitView |
| apple-009 | adaptive-navigation | Run LitterboxTestiOS on iPhone | Root view is NavigationStack |
| apple-010 | navigable-component-list | Launch any target with components registered | Catalog lists all components, selecting one navigates to detail |
| apple-011 | all-states-per-component | View a catalog entry | All states from spec are displayed in labeled sections |
| apple-012 | os-compilation-conditions | Build Shared/ code for all 5 platforms | No compilation errors from platform-specific API usage |

## Edge Cases

- **No components implemented yet**: Catalog SHOULD show an empty state message (e.g., "No components yet") rather than a blank screen.
- **Component only valid on some platforms**: Use `#if os(...)` around the catalog entry registration. The catalog on excluded platforms SHOULD NOT show that component.
- **XcodeGen not installed**: Build commands SHOULD fail with a clear error. Prerequisites section documents the install step.
- **visionOS SDK not installed**: The visionOS target will fail to build. This is acceptable — the other four targets SHOULD still build independently.

## Logging

Subsystem: `{{bundle_id}}` | Category: `ComponentCatalog`

| Event | Level | Message |
|-------|-------|---------|
| Catalog launched | debug | `ComponentCatalog: launched with {{count}} components` |
| Component selected | debug | `ComponentCatalog: selected "{{name}}"` |
| Component not available on platform | debug | `ComponentCatalog: "{{name}}" excluded on {{platform}}` |

## Platform Notes

- **SwiftUI**: This spec is Apple-only. All five targets use SwiftUI exclusively.
- **XcodeGen**: Required for project generation. Install via `brew install xcodegen`. Run `xcodegen generate` from the project directory.
- **Xcode 16+**: Required for visionOS 1.0+ support and latest Swift features.
- **visionOS SDK**: Must be installed separately via Xcode > Settings > Platforms.

## Build, Run, and Verify

### Step 1: Generate

```bash
cd Tests/Projects/Apple && xcodegen generate
```

### Step 2: Build all targets

```bash
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestiOS -destination 'platform=iOS Simulator,name=iPhone 17 Pro' build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestMac build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestWatch -destination 'platform=watchOS Simulator,name=Apple Watch Series 11 (46mm)' build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestTV -destination 'platform=tvOS Simulator,name=Apple TV 4K (3rd generation)' build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestVision -destination 'platform=visionOS Simulator,name=Apple Vision Pro' build
```

### Step 3: Run and verify logs

Launch the macOS app (fastest for iteration) and stream logs to verify spec-defined messages:

```bash
# In one terminal: stream logs filtered to the test app subsystem
log stream --predicate 'subsystem == "com.litterbox.test.mac"' --level debug

# In another terminal: launch the app
open /Users/$USER/Library/Developer/Xcode/DerivedData/LitterboxTests-*/Build/Products/Debug/LitterboxTestMac.app
```

Verify these log messages appear:
- `ComponentCatalog: launched with N components` — on app launch
- `ComponentCatalog: selected "ComponentName"` — when selecting a catalog entry

For simulator targets, use `xcrun simctl` to launch and check logs:

```bash
# Boot simulator and launch app
xcrun simctl boot "iPhone 17 Pro"
xcrun simctl launch --console-pty booted com.litterbox.test.ios
```

### Step 4: Test accessibility options

After verifying basic functionality, test with accessibility options toggled:

```bash
# Test with RTL layout
xcrun simctl spawn booted defaults write com.litterbox.test.ios AppleTextDirection -bool YES
xcrun simctl spawn booted defaults write com.litterbox.test.ios NSForceRightToLeftWritingDirection -bool YES

# Test with increased text size (accessibility large)
xcrun simctl spawn booted defaults write com.litterbox.test.ios UIPreferredContentSizeCategoryName UICTContentSizeCategoryAccessibilityExtraLarge

# Reset after testing
xcrun simctl spawn booted defaults delete com.litterbox.test.ios AppleTextDirection
xcrun simctl spawn booted defaults delete com.litterbox.test.ios NSForceRightToLeftWritingDirection
xcrun simctl spawn booted defaults delete com.litterbox.test.ios UIPreferredContentSizeCategoryName
```

On macOS, toggle Reduce Motion and other options in System Settings > Accessibility to verify component responses.

## Prerequisites

- Xcode 16+
- xcodegen (`brew install xcodegen`)
- visionOS SDK (install via Xcode > Settings > Platforms)

## Design Decisions

_None yet — decisions made during generation should be recorded here._

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

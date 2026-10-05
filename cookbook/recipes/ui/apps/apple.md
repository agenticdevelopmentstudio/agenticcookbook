---
id: c5778e2d-2f3b-4cbd-809b-39ed4b57ff57
title: "Apple Test App Suite"
domain: agenticdevelopercookbook://recipes/ui/apps/apple
type: recipe
version: 2.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
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
ingredients:
  - agenticdevelopercookbook://ingredients/ui/apps/xcodegen-apple-project
  - agenticdevelopercookbook://ingredients/ui/apps/component-catalog
  - agenticdevelopercookbook://ingredients/infrastructure/logging
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Apple Test App Suite

## Overview

An XcodeGen-generated Xcode project with app targets for all five Apple platforms, each displaying a component catalog: a navigable list of every UI component implemented from `ui/` specs, showing all states for visual testing and snapshot verification. The XcodeGen Apple Project ingredient provides the targets, shared package, and source layout; the Component Catalog ingredient provides what each app shows. The recipe wires them together through a shared source directory and per-platform entry points.

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| XcodeGen Apple Project | `agenticdevelopercookbook://ingredients/ui/apps/xcodegen-apple-project` | Five app targets, TestSharedKit package, project.yml, source layout | Yes | Output `Tests/Projects/Apple/` |
| Component Catalog | `agenticdevelopercookbook://ingredients/ui/apps/component-catalog` | Root catalog view, adaptive navigation, per-component state entries | Yes | Navigation style per platform |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Logger used for catalog events | Yes | Category `ComponentCatalog` |

## Integration Requirements

- **shared-source-directory**: A `Shared/` directory MUST be added as a source directory to all targets. It contains:
  - `Shared/Components/` — component implementations from `ui/` specs
  - `Shared/Catalog/` — catalog views showing all states per component
- **os-compilation-conditions**: Platform-specific adaptations within shared code MUST use `#if os(...)` compilation conditions.
- **entry-point-shows-catalog**: Each platform's app entry point (the file under `Sources/{platform}/`) MUST present the Component Catalog's `ComponentCatalogView` as its root view.
- **catalog-in-shared-dir**: The catalog implementation MUST live in `Shared/Catalog/` and component implementations in `Shared/Components/`, so all five targets compile the same catalog source.
- **catalog-logging-via-shared-logger**: Catalog events MUST be logged through the `logging` ingredient with category `ComponentCatalog`.

## Layout

```
Tests/Projects/Apple/              <- XcodeGen Apple Project
├── project.yml
├── TestSharedKit/
├── Sources/{iOS,macOS,watchOS,tvOS,visionOS}/   <- entry point per platform
└── Shared/                        <- compiled into every target
    ├── Components/                <- component implementations
    └── Catalog/                   <- Component Catalog entries

 App entry point -> ComponentCatalogView -> catalog entry -> component in each state
```

Not a visual layout: the diagram shows how the project structure and catalog compose. Navigation layout per platform is defined by the Component Catalog ingredient.

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Component registry | `Shared/Components/` implementations | Component Catalog entries | one-way | Entries registered in `ComponentCatalogView` |
| Platform conditions | Compilation (`#if os(...)`) | Catalog registration | one-way | Entries for unsupported platforms are excluded at compile time |
| Deployment versions | `project.yml` | TestSharedKit and all targets | one-way | One version table applied to every target and the package |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| apple-003 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestiOS | Build succeeds, app launches with catalog |
| apple-004 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestMac | Build succeeds, app launches with catalog |
| apple-005 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestWatch | Build succeeds, app launches with catalog |
| apple-006 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestTV | Build succeeds, app launches with catalog |
| apple-007 | standalone-swiftui-apps, depend-on-shared-kit | Build LitterboxTestVision | Build succeeds, app launches with catalog |
| apple-012 | os-compilation-conditions | Build Shared/ code for all 5 platforms | No compilation errors from platform-specific API usage |
| apple-013 | entry-point-shows-catalog, catalog-in-shared-dir | Launch any target after adding a component through the adding-component-steps | The catalog lists the component and its entry view displays all spec states |
| apple-014 | catalog-logging-via-shared-logger | Launch LitterboxTestMac and select a component | Logs show `ComponentCatalog: launched with N components` and `ComponentCatalog: selected "ComponentName"` |

## Edge Cases

- **Component added on one platform only**: When a component is registered under `#if os(...)`, the project MUST still build for the other four targets, and the catalog on the excluded platforms MUST omit it.
- **Missing visionOS SDK with new components**: Adding a component while the visionOS SDK is absent MUST NOT block building and verifying the other four targets.
- **Empty `Shared/Catalog/`**: With no catalog entries, every target MUST still build and show the catalog's empty state rather than a blank screen.

## Platform Notes

- **SwiftUI**: This recipe is Apple-only. All five targets use SwiftUI exclusively.
- **XcodeGen**: Required for project generation. Install via `brew install xcodegen`. Run `xcodegen generate` from the project directory.
- **Xcode 16+**: Required for visionOS 1.0+ support and latest Swift features.
- **visionOS SDK**: Must be installed separately via Xcode > Settings > Platforms.
- **Compose and React/Web**: Not applicable — this recipe generates an Xcode project for Apple platforms only.

### Build, Run, and Verify

#### Step 1: Generate

```bash
cd Tests/Projects/Apple && xcodegen generate
```

#### Step 2: Build all targets

```bash
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestiOS -destination 'platform=iOS Simulator,name=iPhone 17 Pro' build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestMac build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestWatch -destination 'platform=watchOS Simulator,name=Apple Watch Series 11 (46mm)' build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestTV -destination 'platform=tvOS Simulator,name=Apple TV 4K (3rd generation)' build
xcodebuild -project LitterboxTests.xcodeproj -scheme LitterboxTestVision -destination 'platform=visionOS Simulator,name=Apple Vision Pro' build
```

#### Step 3: Run and verify logs

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

#### Step 4: Test accessibility options

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

### Prerequisites

- Xcode 16+
- xcodegen (`brew install xcodegen`)
- visionOS SDK (install via Xcode > Settings > Platforms)

## Design Decisions

**Decision**: Split the suite into a project ingredient and a catalog ingredient.
**Rationale**: Build configuration and catalog behavior change independently; the catalog can be reused in a differently built project.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [post-generation-verification](agenticdevelopercookbook://guidelines/testing/post-generation-verification) | partial | Testing |
| [previews](agenticdevelopercookbook://guidelines/testing/previews) | partial | Testing |
| [snapshot-testing](agenticdevelopercookbook://guidelines/testing/snapshot-testing) | partial | Testing |

> Status is `partial`: this recipe specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-10-04 | Mike Fullerton | Restructured into recipe shape: composes xcodegen-apple-project and component-catalog |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

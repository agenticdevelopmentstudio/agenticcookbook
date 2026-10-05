---
id: 7DE8CD27-E532-4992-9296-0A6DC1AD1816
title: "XcodeGen Apple Project"
domain: agenticdevelopercookbook://ingredients/ui/apps/xcodegen-apple-project
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "XcodeGen-generated project with five standalone SwiftUI app targets and a shared local Swift package"
platforms:
  - ios
  - macos
  - swift
tags:
  - apple
  - build
  - xcodegen
depends-on: []
related:
  - agenticdevelopercookbook://ingredients/ui/apps/component-catalog
  - agenticdevelopercookbook://recipes/ui/apps/apple
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# XcodeGen Apple Project

## Overview

An XcodeGen-generated Xcode project with one standalone SwiftUI app target per Apple platform (iOS, macOS, watchOS, tvOS, visionOS) and a local Swift package, TestSharedKit, shared by all five. A single `project.yml` is the source of truth; the generated project is output to `Tests/Projects/Apple/`. This ingredient owns project structure, targets, and source layout; what the apps display is the Component Catalog ingredient.

### Terminology

| Term | Definition |
|------|-----------|
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

## Edge Cases

- **XcodeGen not installed**: Build commands SHOULD fail with a clear error. Prerequisites section documents the install step.
- **visionOS SDK not installed**: The visionOS target will fail to build. This is acceptable — the other four targets SHOULD still build independently.

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `name` | string | `LitterboxTests` | Generated project name |
| `bundleIdPrefix` | string | `com.litterbox.test` | Prefix for every target bundle ID |
| `deploymentTarget` | map | iOS 17.0, macOS 14.0, watchOS 10.0, tvOS 17.0, visionOS 1.0 | Minimum OS versions, also applied to TestSharedKit |
| `outputDirectory` | path | `Tests/Projects/Apple/` | Where the project is generated |

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

## Logging

Not applicable: this ingredient defines project structure and build configuration and emits no runtime logs; the Component Catalog ingredient defines the catalog log events.

## Platform Notes

- **SwiftUI**: This ingredient is Apple-only. All five targets use SwiftUI exclusively.
- **XcodeGen**: Required for project generation. Install via `brew install xcodegen`. Run `xcodegen generate` from the project directory.
- **Xcode 16+**: Required for visionOS 1.0+ support and latest Swift features.
- **visionOS SDK**: Must be installed separately via Xcode > Settings > Platforms.
- **Compose and React/Web**: Not applicable — the project is an Xcode project for Apple platforms only.

## Design Decisions

**Decision**: Generate the Xcode project from `project.yml` with XcodeGen instead of checking in an `.xcodeproj`.
**Rationale**: The generated project is reproducible and diffable; only the declarative file is reviewed (single source of truth).
**Approved**: pending

**Decision**: The visionOS target MAY fail to build when its SDK is missing; the other four targets still build independently.
**Rationale**: A missing optional SDK should not block work on the other platforms.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [platform-compliance](agenticdevelopercookbook://compliance/platform-compliance) | partial | Platform |
| [post-generation-verification](agenticdevelopercookbook://guidelines/testing/post-generation-verification) | partial | Testing |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Apple Test App Suite recipe |

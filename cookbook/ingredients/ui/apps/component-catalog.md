---
id: E7419774-543C-4B3E-8C92-9EF6DAD3BB0F
title: "Component Catalog"
domain: agenticdevelopercookbook://ingredients/ui/apps/component-catalog
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Navigable component catalog showing every UI component in all of its spec-defined states, with platform-adaptive navigation"
platforms:
  - ios
  - macos
  - swift
tags:
  - apple
  - catalog
  - ui
depends-on: []
related:
  - agenticdevelopercookbook://ingredients/ui/apps/xcodegen-apple-project
  - agenticdevelopercookbook://recipes/ui/apps/apple
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Component Catalog

## Overview

A navigable catalog of every implemented UI component, showing each component in all the states its spec defines so they can be reviewed visually and verified with snapshots. The root `ComponentCatalogView` adapts its navigation to the platform; each entry view lays out one component's states in labeled sections and carries a preview. This ingredient owns the catalog behavior and the procedure for adding a component; the project that builds it is the XcodeGen Apple Project ingredient.

### Terminology

| Term | Definition |
|------|-----------|
| Catalog | A navigable list of all implemented components, each showing every state from its spec |
| Catalog entry | A single view showing one component in all its states |

## Behavioral Requirements

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

## Appearance

Each catalog entry shows one component per labeled section, one section per state defined in its spec. The visual appearance of the components themselves is defined by their own specs, not by the catalog.

## States

Not applicable — the catalog has no states of its own beyond navigation selection; app-level states (launching, active, background, terminated) are defined by the platform. See `recipes/app/lifecycle.md` for app state management.

## Accessibility

Not applicable — the catalog adds no accessibility requirements of its own. Accessibility requirements are defined per-component in the UI ingredients that the catalog displays.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| apple-008 | adaptive-navigation | Run LitterboxTestMac | Root view is NavigationSplitView |
| apple-009 | adaptive-navigation | Run LitterboxTestiOS on iPhone | Root view is NavigationStack |
| apple-010 | navigable-component-list | Launch any target with components registered | Catalog lists all components, selecting one navigates to detail |
| apple-011 | all-states-per-component | View a catalog entry | All states from spec are displayed in labeled sections |

## Edge Cases

- **No components implemented yet**: Catalog SHOULD show an empty state message (e.g., "No components yet") rather than a blank screen.
- **Component only valid on some platforms**: Use `#if os(...)` around the catalog entry registration. The catalog on excluded platforms SHOULD NOT show that component.

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `navigationStyle` | enum | `NavigationSplitView` on macOS, iPadOS, visionOS; `NavigationStack` on iPhone, watchOS, tvOS | Navigation container chosen by platform |
| `registeredComponents` | list | empty | Catalog entries registered in `ComponentCatalogView` |
| `logCategory` | string | `ComponentCatalog` | Logging category for catalog events |

## Logging

Subsystem: `{{bundle_id}}` | Category: `ComponentCatalog`

| Event | Level | Message |
|-------|-------|---------|
| Catalog launched | debug | `ComponentCatalog: launched with {{count}} components` |
| Component selected | debug | `ComponentCatalog: selected "{{name}}"` |
| Component not available on platform | debug | `ComponentCatalog: "{{name}}" excluded on {{platform}}` |

## Platform Notes

- **SwiftUI**: All catalog views are SwiftUI. Use `NavigationSplitView` or `NavigationStack` per adaptive-navigation, and gate platform-specific entries with `#if os(...)`.
- **Compose and React/Web**: Not applicable — the catalog targets Apple platforms only.

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

## Design Decisions

**Decision**: Every catalog entry shows every state from its component spec in its own labeled section.
**Rationale**: Visual verification and snapshot testing both depend on states being individually reachable on screen.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [previews](agenticdevelopercookbook://guidelines/testing/previews) | partial | Testing |
| [snapshot-testing](agenticdevelopercookbook://guidelines/testing/snapshot-testing) | partial | Testing |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Apple Test App Suite recipe |

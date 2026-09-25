---
type: ingredient
status: accepted
version: 1.1.0
modified: 2026-09-20
platforms: [typescript, web, swift, macos]
domain: mini-repo://recipes/button
---

## Overview

Button component fixture.

## Behavioral Requirements

Button must respond to click events.

## Appearance

Button displays text and optional icon.

## States

Button has default, hover, and active states.

## Accessibility

Button is keyboard accessible.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|----|----|----|
| button-001 | case-1 | input 1 | output 1 |
| button-002 | case-2 | input 2 | output 2 |
| button-003 | case-3 | input 3 | output 3 |
| button-004 | case-4 | input 4 | output 4 |
| button-005 | case-5 | input 5 | output 5 |

## Edge Cases

Button handles long text gracefully.

## Configuration

Button accepts size and color props.

## Deep Linking

Buttons are not deep-link targets.

## Localization

The label is a localized string key.

## Accessibility Options

Increase Contrast raises the border contrast.

## Feature Flags

None.

## Analytics

`button.clicked` fires on activation.

## Privacy

- **Data collected**: None.

## Logging

Debug-level `Button: activated`.

## Platform Notes

- **SwiftUI**: Use `Button` with a custom `ButtonStyle`.
- **Compose**: `Button` with `ButtonDefaults.buttonColors`.
- **React/Web**: `packages/ui/button.tsx`.
- **AppKit / UIKit**: `NSButton` bezel style `.rounded`.
- **WinUI 3**: `Microsoft.UI.Xaml.Controls.Button` with the `AccentButtonStyle` resource.

## Design Decisions

**Decision**: Button uses semantic colors.
**Rationale**: Consistency across the product.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [separation-of-concerns](agenticdevelopercookbook://compliance/best-practices#separation-of-concerns) | passed | best-practices |
| [unit-test-coverage](agenticdevelopercookbook://compliance/best-practices#unit-test-coverage) | passed | best-practices |

The button keeps rendering and behavior apart and is covered by unit tests.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-09-20 | Fixture Author | Filled every template section |
| 1.0.0 | 2026-09-01 | Fixture Author | Initial creation |

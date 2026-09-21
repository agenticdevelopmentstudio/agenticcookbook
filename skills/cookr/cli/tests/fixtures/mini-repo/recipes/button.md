---
type: ingredient
status: accepted
domain: fixture://recipes/button
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

Button passes accessibility tests.

## Edge Cases

Button handles long text gracefully.

## Configuration

Button accepts size and color props.

## Platform Notes

- **SwiftUI**: Use `Button` with a custom `ButtonStyle`.
- **Compose**: `Button` with `ButtonDefaults.buttonColors`.
- **React/Web**: `packages/ui/button.tsx`.
- **AppKit / UIKit**: `NSButton` bezel style `.rounded`.
- **WinUI 3**: `Microsoft.UI.Xaml.Controls.Button` with the `AccentButtonStyle` resource.

## Design Decisions

Button uses semantic colors for consistency.

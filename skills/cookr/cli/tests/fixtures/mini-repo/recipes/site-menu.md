---
type: recipe
status: accepted
---

## Overview

Site menu recipe fixture.

## Ingredients

Site menu uses button and icon components.

## Integration Requirements

Site menu must integrate with navigation system.

## Layout

Site menu arranges buttons in horizontal layout.

## Shared State

Site menu shares active state with router.

## Integration Test Vectors

Site menu passes navigation tests.

## Edge Cases

Site menu handles overflow gracefully.

## Platform Notes

- **SwiftUI**: Use `HStack` with `Button`.
- **Compose**: `Row` with `Button`.
- **React/Web**: `packages/ui/site-menu.tsx`.
- **AppKit / UIKit**: `NSView` with `NSButton`.
- **WinUI 3**: `StackPanel` with `Button`.

## Design Decisions

Site menu uses consistent spacing between items.

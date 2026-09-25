---
domain: mini-repo://cookbook/blocks/stat-card
type: ingredient
status: draft
---

## Overview

Stat card component fixture.

## Behavioral Requirements

Stat card displays a metric and value.

## Appearance

Stat card shows number in large font.

## States

Stat card has default and loading states.

## Accessibility

Stat card is readable by screen readers.

## Conformance Test Vectors

Stat card passes metric display tests.

## Edge Cases

NEEDS REVIEW: Not implemented in source. Behavior undefined.

## Configuration

Stat card accepts metric name and value.

## Platform Notes

- **SwiftUI**: Use `VStack` with `Text`.
- **Compose**: `Row` with `Text`.
- **React/Web**: `packages/ui/stat-card.tsx`.
- **AppKit / UIKit**: `NSView` with labels.
- **WinUI 3**: `StackPanel` with `TextBlock`.

## Reference Implementations

| Platform | Path |
|----------|------|
| web | `web/blocks/StatCard.tsx` |

## Design Decisions

Stat card uses monospace font for numbers.

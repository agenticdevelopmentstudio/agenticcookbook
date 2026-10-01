---
domain: mini-repo://cookbook/site-menu
type: recipe
status: accepted
version: 1.1.1
modified: 2026-09-25
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

| ID | Requirements | Input | Expected |
|----|----|----|----|
| site-menu-001 | case-1 | input 1 | output 1 |
| site-menu-002 | case-2 | input 2 | output 2 |
| site-menu-003 | case-3 | input 3 | output 3 |
| site-menu-004 | case-4 | input 4 | output 4 |
| site-menu-005 | case-5 | input 5 | output 5 |

## Edge Cases

Site menu handles overflow gracefully.

## Platform Notes

- **SwiftUI**: Use `HStack` with `Button`.
- **Compose**: `Row` with `Button`.
- **React/Web**: `packages/ui/site-menu.tsx`.
- **AppKit / UIKit**: `NSView` with `NSButton`.
- **WinUI 3**: `StackPanel` with `Button`.

## Reference Implementations

| Platform | Path |
|----------|------|

## Design Decisions

**Decision**: Site menu uses consistent spacing between items.
**Rationale**: Consistency across the product.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [separation-of-concerns](agenticdevelopercookbook://compliance/best-practices#separation-of-concerns) | passed | best-practices |
| [unit-test-coverage](agenticdevelopercookbook://compliance/best-practices#unit-test-coverage) | passed | best-practices |

The site menu keeps rendering and behavior apart and is covered by unit tests.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-09-25 | Fixture | Moved into the library cookbook; added Reference Implementations. |
| 1.1.0 | 2026-09-20 | Fixture Author | Filled every template section |
| 1.0.0 | 2026-09-01 | Fixture Author | Initial creation |

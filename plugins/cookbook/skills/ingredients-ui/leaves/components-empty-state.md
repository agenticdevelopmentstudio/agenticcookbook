<!-- leaf: ingredients-ui/components-empty-state · source: ingredients/ui/components/empty-state.md -->

**Rules** (cite as `ingredients-ui/components-empty-state#<slug>`):

- `centered-layout` MUST
- `icon-and-heading` MUST
- `optional-description` MAY
- `optional-action-buttons` MAY
- `prominent-primary-action` SHOULD
- `adaptive-container-fit` MUST
- `native-unavailable-view` SHOULD
- `platform-native-icon` MUST
- `heading-first-announce` MUST
- `descriptive-button-labels` MUST
- `decorative-icon` SHOULD

# Empty State

## Overview

A centered placeholder view shown when there is no content to display. Used for: empty lists, no search results, no selection in a split view, first-launch with no data, error states, or any view that needs to communicate "nothing here yet" with an optional call to action.

## Behavioral Requirements

- **centered-layout**: The empty state MUST be centered both horizontally and vertically within its container.
- **icon-and-heading**: The empty state MUST display at minimum an icon and a heading.
- **optional-description**: The empty state MAY display a description below the heading for additional context.
- **optional-action-buttons**: The empty state MAY display one or more action buttons below the description.
- **prominent-primary-action**: If action buttons are present, the primary action SHOULD be visually prominent (filled/borderedProminent style).
- **adaptive-container-fit**: The empty state MUST adapt to the container's available space — it MUST NOT overflow or require scrolling in typical container sizes.
- **native-unavailable-view**: On Apple platforms (iOS 17+, macOS 14+), implementations SHOULD use the native `ContentUnavailableView` as the base control.
- **platform-native-icon**: The icon MUST use a platform-native symbol (SF Symbol on Apple, Material Icon on Android, inline SVG on Web).

## Appearance

- **Icon**: 48pt system symbol, secondary color
- **Heading**: Title3 weight semibold (Apple), Headline5 (Material), h3 (Web)
- **Description**: Subheadline/body, secondary/tertiary color, max 2 lines, centered
- **Action buttons**: Standard platform button styles, 8pt spacing between multiple buttons
- **Vertical spacing**: 8pt icon→heading, 4pt heading→description, 16pt description→buttons
- **Max content width**: 280pt (prevents overly wide text on large screens)

## Accessibility

- **heading-first-announce**: The heading MUST be the first element announced by screen readers.
- **descriptive-button-labels**: Action buttons MUST have descriptive labels (not just "Go" or "OK").
- **decorative-icon**: The icon SHOULD be decorative (`accessibilityHidden(true)`) since the heading conveys the meaning.

## Configuration

This ingredient has no configurable options.

## Platform Notes

- **SwiftUI**: Use `ContentUnavailableView(label:description:actions:)` on iOS 17+/macOS 14+. For older targets, use `VStack` with centered alignment in a `GeometryReader`.
- **Compose**: Use `Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally)` with `Icon`, `Text`, `Button` composables.
- **React/Web**: Centered `<div>` with flexbox `align-items: center; justify-content: center`. Use semantic heading tags (`<h3>`) and `<button>` elements.

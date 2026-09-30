<!-- leaf: ingredients-ui/components-collapsible-pane-header · source: ingredients/ui/components/collapsible-pane-header.md -->

**Rules** (cite as `ingredients-ui/components-collapsible-pane-header#<slug>`):

- `tap-toggles-pane` MUST
- `chevron-animation` MUST
- `collapse-expand-animation` MUST
- `display-title` MUST
- `optional-leading-icon` MAY
- `optional-subtitle` MAY
- `header-always-visible` MUST
- `persist-collapse-state` MUST
- `button-role-label` MUST
- `announce-collapse-state` MUST
- `keyboard-toggle` MUST

# Collapsible Pane Header

## Overview

A clickable header bar with a disclosure chevron that collapses or expands a section of a split view. Used at the top of split pane sections (e.g., editor pane, terminal pane, sidebar) to let the user hide/show content areas. Common in IDE-style multi-pane layouts.

## Behavioral Requirements

- **tap-toggles-pane**: Tapping anywhere on the header MUST toggle the associated pane's visibility.
- **chevron-animation**: The disclosure chevron MUST animate between collapsed (pointing right) and expanded (pointing down) states.
- **collapse-expand-animation**: The pane collapse/expand MUST animate with an ease-in-out curve (~0.2s duration).
- **display-title**: The header MUST display a title.
- **optional-leading-icon**: The header MAY display an icon to the left of the title (e.g., a file icon for an editor pane header).
- **optional-subtitle**: The header MAY display a subtitle or secondary label to the right of the title (e.g., a filename).
- **header-always-visible**: The header MUST remain visible when the pane is collapsed — it is the mechanism to re-expand.
- **persist-collapse-state**: The collapsed/expanded state MUST be persisted per-pane so it survives app restart.

## Appearance

- **Height**: 24–28pt (compact, does not waste vertical space)
- **Background**: System tertiary background / subtle separator color
- **Chevron**: 10pt system disclosure indicator, leading edge, secondary color
- **Title**: Caption or footnote weight medium, primary color
- **Icon** (optional): 12pt system symbol, leading, before title
- **Subtitle** (optional): Caption weight regular, secondary color, trailing
- **Padding**: 6pt vertical, 8pt horizontal
- **Cursor**: Pointer cursor on hover (macOS)

## Accessibility

- **button-role-label**: The header MUST be a button role with label describing the action: "Collapse {{title}}" or "Expand {{title}}".
- **announce-collapse-state**: The expanded/collapsed state MUST be announced: `accessibilityValue("expanded")` or `accessibilityValue("collapsed")`.
- **keyboard-toggle**: The header MUST be keyboard-focusable and toggleable via Return/Space.

## Configuration

This ingredient has no configurable options.

## Platform Notes

- **SwiftUI (macOS)**: `HStack` with `Image(systemName: "chevron.right").rotationEffect(isExpanded ? .degrees(90) : .degrees(0))`. Use `.onTapGesture` on the entire `HStack`. Persist via `@AppStorage` or project settings binding. Animate with `.animation(.easeInOut(duration: 0.2), value: isExpanded)`.
- **SwiftUI (iOS/visionOS)**: Same pattern, useful in `HSplitView` or custom multi-pane layouts.
- **Compose**: `Row` with `Icon` (animated rotation via `animateFloatAsState`). Click on entire row. Persist via `rememberSaveable` or preferences.

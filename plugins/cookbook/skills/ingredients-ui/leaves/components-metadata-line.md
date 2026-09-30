<!-- leaf: ingredients-ui/components-metadata-line · source: ingredients/ui/components/metadata-line.md -->

**Rules** (cite as `ingredients-ui/components-metadata-line#<slug>`):

- `icon-and-text-line` MUST
- `truncation-with-ellipsis` MUST
- `platform-native-icon` MUST
- `optional-tooltip` SHOULD
- `secondary-text-color` MUST
- `vertical-center-alignment` MUST
- `combined-a11y-element` MUST
- `full-text-a11y-label` MUST

# Metadata Line

## Overview

A compact, single-line label combining a leading icon with a text value. Used to display metadata: file paths, git branches, process names, timestamps, status indicators. A fundamental building block for list rows, sidebars, and inspector panels.

## Behavioral Requirements

- **icon-and-text-line**: The component MUST display a leading icon and a text label on a single line.
- **truncation-with-ellipsis**: The text MUST truncate with an ellipsis when it exceeds available width. The truncation position SHOULD be configurable: head, middle, or tail (default: tail).
- **platform-native-icon**: The icon MUST be a platform-native symbol (SF Symbol, Material Icon, or inline SVG).
- **optional-tooltip**: The component SHOULD support an optional tooltip showing the full, untruncated text (desktop platforms).
- **secondary-text-color**: The component MUST use secondary/tertiary text color by default to visually recede as metadata.
- **vertical-center-alignment**: The icon and text MUST be vertically centered on the same baseline.

## Appearance

- **Icon**: 12pt system symbol, secondary color
- **Text**: Caption/caption2, secondary color, single line
- **Spacing**: 4pt between icon and text
- **Height**: Natural text height (~16–18pt)
- **Truncation**: Configurable (`.head`, `.middle`, `.tail`)

## Accessibility

- **combined-a11y-element**: The component MUST be a single accessibility element combining icon meaning and text into one label (e.g., "Branch: main" not "branch icon" then "main").
- **full-text-a11y-label**: If the text is truncated, the accessibility label MUST contain the full text.

## Configuration

This ingredient has no configurable options.

## Platform Notes

- **SwiftUI**: `Label("text", systemImage: "icon").labelStyle(.titleAndIcon)` or custom `HStack { Image(systemName:) Text() }` with `.lineLimit(1).truncationMode()`.
- **Compose**: `Row(verticalAlignment = Alignment.CenterVertically) { Icon(); Spacer(4.dp); Text(maxLines = 1, overflow = TextOverflow.Ellipsis) }`.
- **React/Web**: `<span>` with flexbox `display: inline-flex; align-items: center; gap: 4px`. CSS `text-overflow: ellipsis; white-space: nowrap; overflow: hidden`.

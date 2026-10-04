---
id: d4b2fbc3-d814-44f7-a1cf-b59bd5eeb757
title: "Metadata Line"
domain: agenticdevelopercookbook://ingredients/ui/components/metadata-line
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-05
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compact single-line label combining a leading icon with a text value for displaying metadata"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
tags:
  - component
  - metadata-line
  - ui
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

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

## States

| State | Appearance |
|-------|-----------|
| Default | Icon + text in secondary color |
| Highlighted | Optional: primary color when parent row is selected |
| Empty value | Hide entirely or show placeholder dash |

## Accessibility

- **combined-a11y-element**: The component MUST be a single accessibility element combining icon meaning and text into one label (e.g., "Branch: main" not "branch icon" then "main").
- **full-text-a11y-label**: If the text is truncated, the accessibility label MUST contain the full text.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| meta-001 | icon-and-text-line | icon: "folder", text: "/Users/me/projects" | Icon + text displayed on one line |
| meta-002 | truncation-with-ellipsis | text: very long path, truncation: middle | Displays "..." in middle of path |
| meta-003 | optional-tooltip | Hover over truncated text on macOS | Tooltip shows full text |
| meta-004 | full-text-a11y-label | VoiceOver on truncated text | Full text announced |

## Edge Cases

- **Empty text**: Component SHOULD hide itself or show a dash placeholder.
- **Very short container**: Icon alone may show if text has zero space — acceptable.
- **RTL languages**: Icon remains on the leading edge (which is right in RTL).

## Configuration

This ingredient has no configurable options.

## Logging

Subsystem: `{{bundle_id}}` | Category: `MetadataLine`

| Event | Level | Message |
|-------|-------|---------|
| Displayed | debug | `MetadataLine: displayed "{{text}}" with icon "{{icon}}"` |

## Platform Notes

- **SwiftUI**: `Label("text", systemImage: "icon").labelStyle(.titleAndIcon)` or custom `HStack { Image(systemName:) Text() }` with `.lineLimit(1).truncationMode()`.
- **Compose**: `Row(verticalAlignment = Alignment.CenterVertically) { Icon(); Spacer(4.dp); Text(maxLines = 1, overflow = TextOverflow.Ellipsis) }`.
- **React/Web**: `<span>` with flexbox `display: inline-flex; align-items: center; gap: 4px`. CSS `text-overflow: ellipsis; white-space: nowrap; overflow: hidden`.

## Design Decisions

_None yet._

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

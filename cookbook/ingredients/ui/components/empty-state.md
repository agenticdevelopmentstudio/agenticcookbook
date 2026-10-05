---
id: ce2af25c-4f18-41ae-91b9-342e363449b3
title: "Empty State"
domain: agenticdevelopercookbook://ingredients/ui/components/empty-state
type: ingredient
version: 1.1.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Centered placeholder view shown when there is no content, with icon, heading, and optional action buttons"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
tags:
  - component
  - empty-state
  - ui
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

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

## States

| State | Appearance |
|-------|-----------|
| Icon + heading only | Minimal empty state |
| With description | Adds context text below heading |
| With single action | One prominent button below |
| With multiple actions | Primary + secondary buttons, stacked or horizontal |
| Loading | Can transition from empty state to content via fade |

## Accessibility

- **heading-first-announce**: The heading MUST be the first element announced by screen readers.
- **descriptive-button-labels**: Action buttons MUST have descriptive labels (not just "Go" or "OK").
- **decorative-icon**: The icon SHOULD be decorative (`accessibilityHidden(true)`) since the heading conveys the meaning.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| empty-001 | centered-layout | Render in a 400×400 container | Content is centered |
| empty-002 | icon-and-heading | Provide icon + heading only | Both displayed, no crash |
| empty-003 | optional-action-buttons | Provide 2 action buttons | Both rendered, primary is prominent |
| empty-004 | adaptive-container-fit | Render in 200×150 container | Content fits without scrolling/overflow |
| empty-005 | native-unavailable-view | Build on macOS 14+ | Uses ContentUnavailableView |
| empty-006 | decorative-icon | Enable VoiceOver, navigate to empty state | Icon is not announced, heading is first |

## Edge Cases

- **Very long heading**: SHOULD truncate to 2 lines max
- **Very long description**: SHOULD truncate to 3 lines max with ellipsis
- **No icon provided**: MUST still display heading (icon is visually expected but not structurally required)
- **Container too small**: Content SHOULD scale down gracefully, not clip

## Configuration

This ingredient has no configurable options.

## Logging

Subsystem: `{{bundle_id}}` | Category: `EmptyState`

| Event | Level | Message |
|-------|-------|---------|
| Displayed | debug | `EmptyState: displayed "{{heading}}"` |
| Action tapped | debug | `EmptyState: action "{{label}}" tapped` |

## Platform Notes

- **SwiftUI**: Use `ContentUnavailableView(label:description:actions:)` on iOS 17+/macOS 14+. For older targets, use `VStack` with centered alignment in a `GeometryReader`.
- **Compose**: Use `Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally)` with `Icon`, `Text`, `Button` composables.
- **React/Web**: Centered `<div>` with flexbox `align-items: center; justify-content: center`. Use semantic heading tags (`<h3>`) and `<button>` elements.

## Design Decisions

_None yet._

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [screen-reader-support](agenticdevelopercookbook://compliance/accessibility#screen-reader-support) | partial | Accessibility |
| [string-externalization](agenticdevelopercookbook://compliance/internationalization#string-externalization) | partial | Internationalization |
| [contrast-ratio](agenticdevelopercookbook://compliance/accessibility#contrast-ratio) | partial | Accessibility |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-10-04 | Mike Fullerton | Conform to the ingredient format: section order, non-standard sections folded into allowed ones, Compliance added |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

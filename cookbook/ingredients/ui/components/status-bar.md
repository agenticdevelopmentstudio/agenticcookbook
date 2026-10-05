---
id: 22729bee-7ab4-4648-aa5a-2beef067d0c3
title: "Status Bar"
domain: agenticdevelopercookbook://ingredients/ui/components/status-bar
type: ingredient
version: 1.1.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Slim animated bar that slides in at the bottom of a view to indicate a background operation is in progress"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
tags:
  - component
  - status-bar
  - ui
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Status Bar

## Overview

A slim, animated bar that slides in at the bottom of a view to indicate a background operation is in progress. Shows an indeterminate spinner and a status text message. Appears during sync, loading, or processing operations and disappears when complete.

## Behavioral Requirements

- **slide-in-animation**: The bar MUST slide in from the bottom edge with an animated transition when an operation begins.
- **slide-out-animation**: The bar MUST slide out with an animated transition when the operation completes.
- **indeterminate-spinner**: The bar MUST display an indeterminate progress spinner (platform-native).
- **status-text-display**: The bar MUST display a status text message describing the current operation.
- **overlay-not-push**: The bar MUST be overlaid on existing content (not push content up).
- **ease-in-out-timing**: The animation MUST use an ease-in-out curve with ~0.3s duration.
- **update-text-while-visible**: The bar SHOULD support updating the status text while visible (e.g., "Scanning..." -> "Scanning 42 files...").
- **non-blocking-interaction**: The bar MUST NOT block interaction with the content beneath it.

## Appearance

- **Height**: 28–32pt
- **Background**: System material / translucent with subtle blur (or opaque secondary background)
- **Spinner**: Platform-native indeterminate `ProgressView` / `CircularProgressIndicator` / CSS spinner, 16pt
- **Text**: Caption, secondary color
- **Spacing**: 8pt between spinner and text
- **Padding**: 8pt horizontal, 4pt vertical
- **Corner radius**: 0 (full-width bar) or 8pt if floating
- **Position**: Bottom edge of container, full width

## States

| State | Appearance |
|-------|-----------|
| Hidden | Not rendered, no space consumed |
| Appearing | Slides in from bottom with opacity fade |
| Visible | Spinner animating, text displayed |
| Text updating | Text cross-fades to new value |
| Disappearing | Slides out to bottom with opacity fade |

## Accessibility

- **announce-appearance**: The bar MUST announce its appearance to screen readers with the status text.
- **polite-live-region**: Status text updates SHOULD be announced as polite live region updates (not interrupting).

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| status-001 | slide-in-animation | Set isSyncing = true | Bar slides in from bottom |
| status-002 | slide-out-animation | Set isSyncing = false | Bar slides out to bottom |
| status-003 | overlay-not-push | Bar visible over scrollable content | Content beneath is still scrollable |
| status-004 | update-text-while-visible | Change text while visible | Text updates without bar re-animating |
| status-005 | non-blocking-interaction | Tap content behind visible bar | Content responds to tap |

## Edge Cases

- **Rapid show/hide**: If the operation completes before the appear animation finishes, the bar SHOULD reverse smoothly (not jump).
- **Very long status text**: Truncate with ellipsis on one line.
- **Multiple overlapping operations**: Show the most recent status text. Bar stays visible until all operations complete.

## Configuration

This ingredient has no configurable options.

## Logging

Subsystem: `{{bundle_id}}` | Category: `StatusBar`

| Event | Level | Message |
|-------|-------|---------|
| Shown | debug | `StatusBar: shown with "{{text}}"` |
| Text updated | debug | `StatusBar: updated to "{{text}}"` |
| Hidden | debug | `StatusBar: hidden` |

## Platform Notes

- **SwiftUI**: Use `.overlay(alignment: .bottom)` with a `Group` that conditionally renders the bar. Transition: `.move(edge: .bottom).combined(with: .opacity)`. Animation: `.easeInOut(duration: 0.3)`. Use `ProgressView()` for spinner.
- **Compose**: `Box(modifier = Modifier.fillMaxSize())` with `AnimatedVisibility(enter = slideInVertically + fadeIn, exit = slideOutVertically + fadeOut)` at bottom. `CircularProgressIndicator(modifier = Modifier.size(16.dp))`.
- **React/Web**: Absolutely positioned `<div>` at `bottom: 0` with CSS transition on `transform: translateY()` and `opacity`. Use CSS `@keyframes spin` for spinner or a library spinner.

## Design Decisions

_None yet._

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [screen-reader-support](agenticdevelopercookbook://compliance/accessibility#screen-reader-support) | partial | Accessibility |
| [contrast-ratio](agenticdevelopercookbook://compliance/accessibility#contrast-ratio) | partial | Accessibility |
| [string-externalization](agenticdevelopercookbook://compliance/internationalization#string-externalization) | partial | Internationalization |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-10-04 | Mike Fullerton | Conform to the ingredient format: section order, non-standard sections folded into allowed ones, Compliance added |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

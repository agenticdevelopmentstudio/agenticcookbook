---
id: 3DC1F9B4-3290-4F81-8903-EDA323DD4336
title: "ComponentName"
domain: agenticdevelopercookbook://ingredients/_template
type: ingredient
version: 1.1.0
status: accepted
language: en
created: 2026-04-05
modified: 2026-09-25
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: ""
platforms: 
  - kotlin
  - swift
  - typescript
  - web
tags: []
depends-on: []
related: []
references: []
approved-by: ""
approved-date: ""
---

# ComponentName

## Overview

Brief description of what this component is and when to use it.

## Behavioral Requirements

- **do-something**: Component MUST ...
- **do-something-else**: Component SHOULD ...
- **do-something-optional**: Component MAY ...

## Appearance

- **Corner radius**:
- **Padding**: vertical × horizontal
- **Font**: weight, size
- **Background**: color value or description
- **Foreground/Text**: color value or description
- **Border**: width, color (if any)
- **Shadow**: offset, blur, color (if any)
- **Min/Max size**: constraints (if any)

## States

| State | Appearance change |
|-------|------------------|
| Default | — |
| Pressed | |
| Disabled | |
| Focused | |
| Loading | |

## Accessibility

- Role/trait (e.g., button, heading, text field)
- Label requirements
- Announce state changes (e.g., loading, disabled)
- Minimum tap target: 44×44pt

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| component-001 | do-something | | |

## Edge Cases

- Describe boundary conditions, error states, unexpected input

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|

## Deep Linking

| Platform | URL Pattern |
|----------|-------------|
| Apple | `{{app_scheme}}://component-name` |
| Android | `https://{{app_domain}}/component-name` |
| Web | `/component-name` |

## Localization

| String Key | Default (en) | Context |
|-----------|-------------|---------|
| | | |

## Accessibility Options

Document which accessibility display options (Rule 15) this component responds to:

| Option | Behavior |
|--------|----------|
| Reduce Motion | |
| Increase Contrast | |
| Differentiate Without Color | |

## Feature Flags

| Flag Key | Default | Description |
|----------|---------|-------------|
| `{{app_prefix}}.component_name` | `true` | Enables this component |

## Analytics

| Event | Properties | When |
|-------|-----------|------|
| `component_name.viewed` | `{}` | Component appears on screen |
| `component_name.interacted` | `{ action: string }` | User interacts with component |

## Privacy

- **Data collected**: None / describe what is collected
- **Storage**: Where and how data is stored
- **Transmission**: Whether data leaves the device
- **Retention**: How long data is kept

## Logging

Subsystem: `{{bundle_id}}` | Category: `ComponentName`

| Event | Level | Message |
|-------|-------|---------|
| | debug | `ComponentName: ` |

## Platform Notes

- **SwiftUI**:
- **Compose**:
- **React/Web**:
- **AppKit / UIKit**:
- **WinUI 3**:

## Reference Implementations

| Platform | Path |
|----------|------|
| apple | `path/from/repo/root/ComponentName.swift` |
| web | `path/from/repo/root/component-name.tsx` |

Every implementation of this ingredient in the cookbook's own repository, one row per source file or directory, with the path relative to the repository root. A directory row (trailing `/`) claims every source file below it. In a cookbook with no code of its own, write one line instead of the table: `Not applicable: this cookbook carries no implementations.`

## Design Decisions

Record any decisions made during implementation that affect visual or behavioral outcome. Each decision should be approved by the user.

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [check-name](agenticdevelopercookbook://compliance/document#check-name) | passed | Category |

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-09-25 | Mike Fullerton | Library cookbooks: Reference Implementations section and cookbook.json code block |
| 1.0.0 | 2026-04-05 | Mike Fullerton | Initial creation |

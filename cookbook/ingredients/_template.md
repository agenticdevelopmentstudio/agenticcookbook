---
id: 3DC1F9B4-3290-4F81-8903-EDA323DD4336
title: "ComponentName"
type: ingredient
version: 2.0.0
status: accepted
language: en
created: 2026-04-05
modified: 2026-11-09
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

<!-- No `## Reference Implementations` section is authored. Record the code that implements this
ingredient with `cookr implements <uuid|rdid> <location> --platform <p>` and `cookr confirm <uuid|rdid>`;
a compiled doc or skill shows those rows as a derived section here. -->

## Design Decisions

Record any decisions made during implementation that affect visual or behavioral outcome. Each decision should be approved by the user.

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [adc.check.<document>.<check-name>](cookbook:<check-uuid>) | passed | Category |

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-11-09 | Mike Fullerton | cookr format 2: UUID links and rdids; Reference Implementations derived from index.json, not authored |
| 1.1.0 | 2026-09-25 | Mike Fullerton | Library cookbooks: Reference Implementations section and cookbook.json code block |
| 1.0.0 | 2026-04-05 | Mike Fullerton | Initial creation |

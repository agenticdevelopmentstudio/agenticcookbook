---
id: bdc920ab-fde0-445a-a62a-c2f6d23da8a8
title: "Color Profile"
domain: agenticdevelopercookbook://ingredients/ui/components/color-profile
type: ingredient
version: 1.1.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Named color palette with foreground, background, ANSI colors, and built-in presets for terminal and editor theming"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
tags:
  - color-profile
  - component
  - ui
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Color Profile

## Overview

A named color palette defining foreground, background, cursor, selection, and 16 ANSI colors. Used for terminal emulators, code editors, or any component that needs switchable color themes. Includes a set of built-in presets (Solarized, Dracula, Nord, etc.) and supports user-created custom profiles.

## Behavioral Requirements

### Profile structure

- **profile-structure**: Each profile MUST have: a unique ID (UUID), a display name, an appearance preference (dark/light/auto), font name, font size, cursor style, a color palette, and a deletable flag.
- **palette-format**: The color palette MUST contain: foreground, background, cursor, and selection colors as `#rrggbb` hex strings, plus an array of exactly 16 ANSI colors (indices 0–15: 8 normal + 8 bright).

### Built-in profiles

- **built-in-profiles**: The app MUST ship with at least these built-in profiles (non-deletable, non-editable):

  | Name | Appearance | Background | Foreground |
  |------|-----------|-----------|-----------|
  | Solarized Dark | dark | #002b36 | #839496 |
  | Solarized Light | light | #fdf6e3 | #657b83 |
  | Dracula | dark | #282a36 | #f8f8f2 |
  | Nord | dark | #2e3440 | #d8dee9 |
  | Tokyo Night | dark | #1a1b26 | #a9b1d6 |
  | GitHub Light | light | #ffffff | #24292e |
  | Gruvbox Dark | dark | #282828 | #ebdbb2 |
  | Catppuccin Mocha | dark | #1e1e2e | #cdd6f4 |

- **stable-builtin-uuids**: Built-in profiles MUST have stable, fixed UUIDs so references survive app updates.

### User profiles

- **duplicate-profile**: Users MUST be able to duplicate any profile to create a custom copy.
- **editable-custom-profiles**: Custom profiles MUST be editable: name, appearance, font size, cursor style.
- **deletable-custom-only**: Custom profiles MUST be deletable. Built-in profiles MUST NOT be deletable.

### Active profile

- **single-active-profile**: Exactly one profile MUST be active at a time. The active profile ID MUST be persisted in user settings.
- **fallback-to-default**: If the stored active profile ID is invalid (deleted or not found), the app MUST fall back to the first built-in profile (Solarized Dark).

### Appearance mode

- **auto-appearance-mode**: Profiles with `auto` appearance MUST follow the system dark/light mode — using a dark profile when in dark mode and a light profile when in light mode. The specific dark/light mapping is a **Design Decision**.

## Appearance

### Profile list (in settings)

- Each row shows: circular color swatch (background color), profile name, appearance badge (D/L/A)
- Active profile is highlighted
- Built-in profiles grouped first, then custom profiles

### Profile detail editor

- **General**: Name field (editable for custom, read-only for built-in), appearance picker
- **Font**: Font name (read-only), size stepper (range: 8–72pt, default: 13pt)
- **Cursor**: Style picker (block, underline, bar)
- **Colors**: Swatches for FG/BG/cursor/selection, 4×4 grid for 16 ANSI colors
- **Preview**: Sample terminal text with profile colors applied

## States

| State | Behavior |
|-------|----------|
| No custom profiles | Only built-in profiles shown |
| Profile selected | Detail editor shows profile settings |
| Profile duplicated | New profile created with " Copy" suffix, auto-selected |
| Profile deleted | Selection falls back to previous or first built-in |
| Active profile changed | All consumers immediately update their colors |

## Accessibility

- **swatch-a11y-labels**: Color swatches MUST have accessible labels describing the color (e.g., "Background: dark blue").
- **keyboard-navigable-list**: The profile list MUST be keyboard-navigable.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| profile-001 | built-in-profiles | Launch fresh app | 8 built-in profiles available |
| profile-002 | stable-builtin-uuids | Reference Solarized Dark by UUID across updates | UUID is stable |
| profile-003 | duplicate-profile | Duplicate Dracula | New "Dracula Copy" profile created, editable, deletable |
| profile-004 | deletable-custom-only | Attempt to delete Solarized Dark | Delete action disabled/hidden |
| profile-005 | fallback-to-default | Set active profile to invalid UUID | Falls back to Solarized Dark |
| profile-006 | auto-appearance-mode | Set profile to auto, switch system to dark mode | Dark-appropriate colors applied |

## Edge Cases

- **Many custom profiles**: List SHOULD scroll; performance SHOULD remain smooth with 50+ profiles.
- **Profile storage corruption**: Fall back to built-in defaults.
- **Hex color parsing**: `#rrggbb` and `rrggbb` formats MUST both be accepted. Invalid hex returns nil/default.

## Configuration

This ingredient has no configurable options.

## Logging

Subsystem: `{{bundle_id}}` | Category: `ColorProfile`

| Event | Level | Message |
|-------|-------|---------|
| Active profile changed | debug | `ColorProfile: active profile changed to "{{name}}" ({{id}})` |
| Profile duplicated | debug | `ColorProfile: duplicated "{{source}}" as "{{new}}"` |
| Profile deleted | debug | `ColorProfile: deleted "{{name}}" ({{id}})` |
| Fallback to default | debug | `ColorProfile: invalid active ID, falling back to Solarized Dark` |

## Platform Notes

- **Swift**: `struct ColorProfile: Codable, Identifiable, Equatable` with `TerminalColorPalette` sub-struct. Store profiles in `UserDefaults` as JSON or in app's document package. Use `NSColor(hex:)` extension for parsing. Apply to SwiftTerm via `installColors()`.
- **Kotlin**: `data class ColorProfile` with `@Serializable`. Store in SharedPreferences as JSON. Parse hex with `Color(android.graphics.Color.parseColor("#rrggbb"))`.
- **TypeScript**: Interface with hex string fields. Store in localStorage as JSON. Parse with CSS `color` property directly.

## Design Decisions

_None yet._

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [contrast-ratio](agenticdevelopercookbook://compliance/accessibility#contrast-ratio) | partial | Accessibility |
| [platform-theming](agenticdevelopercookbook://compliance/platform-compliance#platform-theming) | partial | Platform |
| [screen-reader-support](agenticdevelopercookbook://compliance/accessibility#screen-reader-support) | partial | Accessibility |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-10-04 | Mike Fullerton | Conform to the ingredient format: section order, non-standard sections folded into allowed ones, Compliance added |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

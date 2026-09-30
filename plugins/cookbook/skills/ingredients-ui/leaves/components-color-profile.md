<!-- leaf: ingredients-ui/components-color-profile · source: ingredients/ui/components/color-profile.md -->

**Rules** (cite as `ingredients-ui/components-color-profile#<slug>`):

- `profile-structure` MUST
- `palette-format` MUST
- `built-in-profiles` MUST
- `stable-builtin-uuids` MUST
- `duplicate-profile` MUST
- `editable-custom-profiles` MUST
- `deletable-custom-only` MUST
- `single-active-profile` MUST
- `fallback-to-default` MUST
- `auto-appearance-mode` MUST
- `swatch-a11y-labels` MUST
- `keyboard-navigable-list` MUST

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

## Accessibility

- **swatch-a11y-labels**: Color swatches MUST have accessible labels describing the color (e.g., "Background: dark blue").
- **keyboard-navigable-list**: The profile list MUST be keyboard-navigable.

## Configuration

This ingredient has no configurable options.

## Platform Notes

- **Swift**: `struct ColorProfile: Codable, Identifiable, Equatable` with `TerminalColorPalette` sub-struct. Store profiles in `UserDefaults` as JSON or in app's document package. Use `NSColor(hex:)` extension for parsing. Apply to SwiftTerm via `installColors()`.
- **Kotlin**: `data class ColorProfile` with `@Serializable`. Store in SharedPreferences as JSON. Parse hex with `Color(android.graphics.Color.parseColor("#rrggbb"))`.
- **TypeScript**: Interface with hex string fields. Store in localStorage as JSON. Parse with CSS `color` property directly.

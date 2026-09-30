<!-- leaf: ingredients-ui/components-git-status-indicator · source: ingredients/ui/components/git-status-indicator.md -->

**Rules** (cite as `ingredients-ui/components-git-status-indicator#<slug>`):

- `supported-statuses` MUST
- `character-badge-display` MUST
- `bold-monospaced-font` MUST
- `optional-text-label` MAY
- `directory-rollup` MUST
- `ancestor-propagation` MUST
- `porcelain-parsing` SHOULD
- `handle-renames` MUST
- `command-timeout` MUST
- `discard-stale-results` MUST
- `full-status-a11y-label` MUST
- `differentiate-without-color` MUST

# Git Status Indicator

## Overview

A semantic representation of git file status with associated colors, display characters, and priority-based directory rollup. Used in file browsers, sidebars, and inspector panels to indicate whether files are modified, added, deleted, etc.

## Behavioral Requirements

### Status types

- **supported-statuses**: The component MUST support these git statuses:

  | Status | Character | Color | Priority |
  |--------|-----------|-------|----------|
  | Modified | M | Orange | 5 |
  | Added | A | Green | 4 |
  | Deleted | D | Red | 3 |
  | Renamed | R | Blue | 2 |
  | Untracked | ? | Green | 1 |
  | Conflicted | U | Purple | 6 (highest) |
  | Ignored | ! | Gray | 0 (lowest) |

### Display

- **character-badge-display**: The status MUST be displayable as a single monospaced character badge with the associated color.
- **bold-monospaced-font**: The badge MUST use a bold, caption-sized monospaced font for the character.
- **optional-text-label**: The badge MAY additionally show a text label (e.g., "Modified") in inspector/detail contexts.

### Directory rollup

- **directory-rollup**: When displaying status for a directory, the component MUST aggregate child file statuses by selecting the highest-priority status. For example, a directory containing both modified (5) and untracked (1) files MUST show modified (5).
- **ancestor-propagation**: The rollup MUST propagate through all ancestor directories up to the root.

### Git status parsing

- **porcelain-parsing**: Status SHOULD be parsed from `git status --porcelain=v1` output (XY format).
- **handle-renames**: Parsing MUST handle renamed files (format: `R  old -> new`) by using the new path.
- **command-timeout**: The git command MUST have a timeout (5 seconds recommended) to prevent hanging on large repos.
- **discard-stale-results**: Stale results MUST be discarded — use request ID tracking to ignore out-of-order responses.

## Appearance

- **Badge**: Monospaced bold caption2, colored per status
- **Inline (in file tree row)**: Right-aligned, single character
- **Detailed (in inspector)**: Character + label (e.g., "M Modified"), colored

## Accessibility

- **full-status-a11y-label**: The badge MUST have an accessibility label with the full status name (e.g., "Modified" not "M").
- **differentiate-without-color**: Color MUST NOT be the only indicator — the character provides differentiation without color (satisfies Rule 15: Differentiate Without Color).

## Configuration

This ingredient has no configurable options.

## Platform Notes

- **SwiftUI**: Status enum with `color: Color` and `displayCharacter: String` computed properties. Use `Text(status.displayCharacter).font(.caption2.monospaced().bold()).foregroundStyle(status.color)`. Git provider runs `Process()` with `git status --porcelain=v1 -uall --ignore-submodules` on a background queue.
- **Compose**: Sealed class with `color: Color` and `char: String` properties. `Text(status.char, color = status.color, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold, fontSize = 10.sp)`.
- **React/Web**: TypeScript enum or union type. `<span style={{ fontFamily: 'monospace', fontWeight: 'bold', color: status.color }}>{status.char}</span>`. Git status via backend API or `simple-git` library in Electron.

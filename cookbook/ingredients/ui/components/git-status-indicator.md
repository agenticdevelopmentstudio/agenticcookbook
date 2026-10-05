---
id: 561a27f4-f019-4d3a-96eb-c18d37b16b61
title: "Git Status Indicator"
domain: agenticdevelopercookbook://ingredients/ui/components/git-status-indicator
type: ingredient
version: 1.1.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Git file status indicator with colored character badges, text labels, and priority-based directory rollup"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
tags:
  - component
  - git-status-indicator
  - ui
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

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

## States

| State | Appearance |
|-------|-----------|
| No git status | Badge not shown |
| File has status | Single character badge with color |
| Directory has aggregated status | Highest-priority child status shown |
| Git command in progress | Previous status remains until new result arrives |
| Git command failed/timed out | Previous status cleared or retained with stale indicator |

## Accessibility

- **full-status-a11y-label**: The badge MUST have an accessibility label with the full status name (e.g., "Modified" not "M").
- **differentiate-without-color**: Color MUST NOT be the only indicator — the character provides differentiation without color (satisfies Rule 15: Differentiate Without Color).

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| git-001 | supported-statuses | File status: modified | Orange "M" badge |
| git-002 | supported-statuses | File status: conflicted | Purple "U" badge |
| git-003 | directory-rollup | Directory with modified + untracked children | Shows modified (priority 5 > 1) |
| git-004 | directory-rollup | Directory with conflicted + modified children | Shows conflicted (priority 6 > 5) |
| git-005 | ancestor-propagation | Deeply nested modified file | All ancestor dirs show modified |
| git-006 | handle-renames | Porcelain output: `R  old.txt -> new.txt` | Status applied to new.txt path |
| git-007 | command-timeout | Git hangs for 6 seconds | Command terminated, no crash |
| git-008 | differentiate-without-color | Grayscale display | Characters (M, A, D, etc.) still distinguish statuses |

## Edge Cases

- **Not a git repo**: No statuses shown, no error.
- **Very large repo (10k+ files)**: `git status` may be slow — timeout protects UI.
- **Rapid file changes**: Debounce git status refresh (0.5s recommended) to prevent thrashing.
- **Submodules**: `--ignore-submodules` flag recommended to avoid deep recursion.
- **Binary files**: Same status handling as text files.

## Configuration

This ingredient has no configurable options.

## Logging

Subsystem: `{{bundle_id}}` | Category: `GitStatus`

| Event | Level | Message |
|-------|-------|---------|
| Refresh started | debug | `GitStatus: refresh started for "{{repoPath}}"` |
| Refresh completed | debug | `GitStatus: refresh completed, {{count}} files with status` |
| Refresh timed out | debug | `GitStatus: refresh timed out after {{timeout}}s` |
| Stale result discarded | debug | `GitStatus: discarded stale result (request {{id}})` |

## Platform Notes

- **SwiftUI**: Status enum with `color: Color` and `displayCharacter: String` computed properties. Use `Text(status.displayCharacter).font(.caption2.monospaced().bold()).foregroundStyle(status.color)`. Git provider runs `Process()` with `git status --porcelain=v1 -uall --ignore-submodules` on a background queue.
- **Compose**: Sealed class with `color: Color` and `char: String` properties. `Text(status.char, color = status.color, fontFamily = FontFamily.Monospace, fontWeight = FontWeight.Bold, fontSize = 10.sp)`.
- **React/Web**: TypeScript enum or union type. `<span style={{ fontFamily: 'monospace', fontWeight: 'bold', color: status.color }}>{status.char}</span>`. Git status via backend API or `simple-git` library in Electron.

## Design Decisions

_None yet._

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [screen-reader-support](agenticdevelopercookbook://compliance/accessibility#screen-reader-support) | partial | Accessibility |
| [contrast-ratio](agenticdevelopercookbook://compliance/accessibility#contrast-ratio) | partial | Accessibility |
| [main-thread-freedom](agenticdevelopercookbook://compliance/performance#main-thread-freedom) | partial | Performance |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-10-04 | Mike Fullerton | Conform to the ingredient format: section order, non-standard sections folded into allowed ones, Compliance added |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

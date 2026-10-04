---
id: a1845427-a2cd-4744-96bf-f6c6f2380982
title: "File Tree Browser"
domain: agenticdevelopercookbook://ingredients/ui/panels/file-tree-browser
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-05
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Hierarchical file browser with lazy loading, git status badges, ignore patterns, and file-type icons"
platforms:
  - ios
  - macos
  - swift
  - typescript
  - web
tags:
  - file-tree-browser
  - panel
  - ui
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# File Tree Browser

## Overview

A hierarchical file browser that displays a project's directory structure using OutlineGroup/List with lazy child loading, git status badges, configurable ignore patterns, and SF Symbol icons themed by file type. Serves as the primary navigation sidebar for project-based workflows.

## Terminology

| Term | Definition |
|------|-----------|
| Node | A single entry in the file tree representing a file or directory |
| Lazy loading | Children of a directory are loaded on demand when the user expands it, not upfront |
| Package | A directory that is treated as a single opaque item (e.g., `.catnip-proj`) and is not expandable |
| Ignore pattern | A POSIX fnmatch()-compatible wildcard pattern (supports `*` and `?`) used to hide matching entries |
| Rollup | Aggregation of git statuses from child files to their parent directory |

## Behavioral Requirements

### Tree display

- **outline-group-hierarchy**: The file tree MUST render using List + OutlineGroup to provide expandable/collapsible directory hierarchy.
- **lazy-child-loading**: The tree MUST use lazy child loading — children MUST be loaded on demand when a directory is expanded, not when the tree is first rendered.
- **parallel-top-level-scan**: Top-level directories MUST be scanned in parallel via OperationQueue for faster initial load.
- **sidebar-list-style**: The tree MUST use `.listStyle(.sidebar)` on Apple platforms.

### Sorting

- **dirs-first-alpha-sort**: Entries MUST be sorted with directories first, then files. Within each group, entries MUST be sorted alphabetically using case-insensitive comparison.

### Filtering and visibility

- **fnmatch-ignore-patterns**: Ignore patterns MUST use POSIX fnmatch() wildcards (`*`, `?`). Entries matching any ignore pattern MUST be hidden from the tree.
- **show-dotfiles**: Hidden files (dotfiles) MUST be shown in the tree.
- **hide-ds-store**: `.DS_Store` files MUST always be hidden regardless of ignore patterns (hardcoded skip).

### Packages

- **package-dir-display**: Directories recognized as packages (e.g., `.catnip-proj` and other registered package extensions) MUST be displayed as single non-expandable items with the package icon.

### Selection

- **single-file-selection**: The tree MUST support single file selection via a selection binding.

### Git status integration

- **git-status-badge**: Each file row MUST display a git status badge when the file has a git status. The badge MUST be right-aligned, use a monospaced font, and be colored per status type. Badge rendering MUST delegate to [git-status-indicator.md](../components/git-status-indicator.md).
- **git-debounce-refresh**: Git status MUST refresh with a 0.5-second debounce after file changes to prevent thrashing.
- **git-background-fetch**: Git status MUST be fetched on a background queue and MUST NOT block the main thread.

### Status bar integration

- **sync-status-bar**: During directory sync operations, a status bar overlay MUST be shown. Display MUST delegate to [status-bar.md](../components/status-bar.md).

### Directory sync lifecycle

- **delegate-directory-sync**: File system monitoring and sync behavior MUST delegate to [directory-sync.md](../../../recipes/infrastructure/directory-sync.md).

## Appearance

### Row layout

```
┌──────────────────────────────────────────────┐
│  📁 Sources                              M   │
│    📄 App.swift                          A   │
│    📄 ContentView.swift                  M   │
│  📁 Tests                                    │
│  📦 MyPlugin.catnip-proj                     │
│  📄 Package.swift                            │
│  📄 README.md                                │
│  📄 .gitignore                               │
└──────────────────────────────────────────────┘
```

- **Row content**: Icon (colored per type) + file name + optional git status badge (right-aligned)
- **File name**: Single line, truncated with middle truncation if too long
- **Tooltip**: Full path of the entry
- **Icon size**: Body-scaled SF Symbol
- **List style**: `.sidebar` on Apple platforms

### Icon theming

#### Packages

| Pattern | SF Symbol | Color |
|---------|-----------|-------|
| Any recognized package directory | `shippingbox.fill` | Orange |

#### Special directories

| Pattern | SF Symbol | Color |
|---------|-----------|-------|
| `.claude` | `brain` | Accent |
| `.git` | `arrow.triangle.branch` | Accent |
| `Sources` or `src` | `folder.fill.badge.gearshape` | Accent |
| `Tests` or `test` | `folder.fill.badge.questionmark` | Accent |
| Dotfile directories (other than above) | `folder.badge.gearshape` | Accent |

#### Files by extension

| Extension(s) | SF Symbol | Color |
|--------------|-----------|-------|
| `.swift` | `swift` | Orange |
| `.json` | `curlybraces` | Yellow |
| `.md`, `.markdown` | `doc.richtext` | Blue |
| `.yaml`, `.yml`, `.toml` | `gearshape.2` | Secondary |
| `.sh`, `.bash`, `.zsh` | `terminal` | Secondary |
| `.py`, `.js`, `.ts`, `.rb` | `chevron.left.forwardslash.chevron.right` | Secondary |

#### Defaults

| Type | SF Symbol | Color |
|------|-----------|-------|
| Directory (no special match) | `folder.fill` | Accent |
| File (no extension match) | `doc` | Secondary |

## States

| State | Behavior |
|-------|----------|
| Initial load | Top-level entries scanned in parallel, tree populates progressively |
| Directory collapsed | Children not loaded (lazy) |
| Directory expanding | Children loaded on demand, disclosure indicator rotates |
| Directory expanded | Children visible, sorted per dirs-first-alpha-sort |
| File selected | Selection highlight, selection binding updated |
| Syncing | Status bar overlay visible (sync-status-bar) |
| Git status loading | Previous badges remain until new results arrive |
| Empty directory | Expanded directory shows no children |
| Ignore pattern matches | Matching entries hidden from tree |

## Accessibility

- **row-accessible-label**: Each row MUST have an accessibility label that includes the entry name and type (file or directory).
- **git-badge-accessible**: Git status badges MUST have accessibility labels with the full status name (e.g., "Modified") rather than the single character.
- **keyboard-tree-nav**: The tree MUST be navigable via keyboard — arrow keys to move between rows, Right arrow to expand, Left arrow to collapse.
- **voiceover-row-announce**: VoiceOver MUST announce the entry name, type, and git status (if any) when a row gains focus.
- **icon-shape-not-color**: Color MUST NOT be the sole differentiator for file type icons — the distinct SF Symbol shapes provide differentiation without color.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| ftb-001 | outline-group-hierarchy | Render tree with nested directories | OutlineGroup renders expandable hierarchy |
| ftb-002 | lazy-child-loading | Expand a collapsed directory | Children loaded at expand time, not before |
| ftb-003 | dirs-first-alpha-sort | Directory with mixed files and subdirs | Subdirs listed first, then files, both alphabetical case-insensitive |
| ftb-004 | fnmatch-ignore-patterns | Ignore pattern `*.log`, directory contains `debug.log` | `debug.log` not visible in tree |
| ftb-005 | fnmatch-ignore-patterns | Ignore pattern `temp?`, directory contains `temp1` and `temp12` | `temp1` hidden, `temp12` visible |
| ftb-006 | show-dotfiles | Directory contains `.env` and `.gitignore` | Both dotfiles visible in tree |
| ftb-007 | hide-ds-store | Directory contains `.DS_Store` | `.DS_Store` not visible in tree |
| ftb-008 | package-dir-display | Directory contains `MyPlugin.catnip-proj` | Shown as non-expandable item with `shippingbox.fill` icon |
| ftb-009 | single-file-selection | Tap/click a file row | Selection binding updates to that file |
| ftb-010 | git-status-badge | File has git status "modified" | Orange "M" badge right-aligned in row |
| ftb-011 | git-debounce-refresh | Three file changes within 0.3s | Git status refreshes once after 0.5s debounce, not three times |
| ftb-012 | dirs-first-alpha-sort | Entries: `zebra/`, `alpha.txt`, `beta/`, `gamma.txt` | Order: `beta/`, `zebra/`, `alpha.txt`, `gamma.txt` |
| ftb-013 | parallel-top-level-scan | Root directory with 5 top-level subdirectories | All 5 scanned in parallel (up to maxScanWorkers) |
| ftb-014 | row-accessible-label, voiceover-row-announce | VoiceOver focus on a modified Swift file | Announces "App.swift, file, Modified" |
| ftb-015 | keyboard-tree-nav | Focus on collapsed directory, press Right arrow | Directory expands |

## Edge Cases

- **Empty project directory**: Tree SHOULD display an empty state rather than a blank sidebar. MAY delegate to an empty-state component.
- **Very deep nesting (20+ levels)**: Tree MUST remain scrollable and responsive. Indentation SHOULD cap or compress at extreme depths.
- **Very large directory (10k+ entries)**: Lazy loading (lazy-child-loading) and parallel scanning (parallel-top-level-scan) mitigate load time. The tree SHOULD remain responsive.
- **Permission denied on directory**: The directory SHOULD show as non-expandable. An error SHOULD be logged but not surfaced to the user as a modal alert.
- **Symlink loops**: The scanner MUST detect and break symlink cycles to prevent infinite recursion.
- **File disappears between scan and display**: The tree SHOULD gracefully handle stale entries — remove them on next refresh rather than crash.
- **Ignore pattern changed while tree is visible**: Tree MUST fully resync to apply new pattern.
- **Directory renamed externally**: Directory sync (delegate-directory-sync) handles this — tree updates on next sync cycle.
- **No git repository**: Git status badges not shown, no error. Tree renders without badges.
- **File tree does NOT include a search/filter UI**: This is noted as a future option and is explicitly out of scope for this spec.

## Configuration

This ingredient has no configurable options.

## Project Settings

| Setting | Type | Default | Constraints | Description |
|---------|------|---------|-------------|-------------|
| `ignorePatterns` | `[String]` | `[]` | POSIX fnmatch() wildcards | Wildcard patterns to hide from the tree |
| `maxScanWorkers` | `Int` | `3` | 1-8 | Maximum parallel scan concurrency for top-level directory scanning |

- **per-project-settings**: Both settings MUST be configured per-project.
- **setting-change-resync**: Changing either setting MUST trigger a full resync of the file tree.

## Logging

Subsystem: `{{bundle_id}}` | Category: `FileTreeBrowser`

| Event | Level | Message |
|-------|-------|---------|
| Tree load started | debug | `FileTreeBrowser: loading tree for "{{rootPath}}"` |
| Tree load completed | debug | `FileTreeBrowser: loaded {{count}} top-level entries` |
| Directory expanded | debug | `FileTreeBrowser: expanded "{{path}}", {{count}} children` |
| Directory collapsed | debug | `FileTreeBrowser: collapsed "{{path}}"` |
| File selected | debug | `FileTreeBrowser: selected "{{path}}"` |
| Ignore pattern applied | debug | `FileTreeBrowser: hiding "{{path}}" (matched pattern "{{pattern}}")` |
| Scan error | error | `FileTreeBrowser: scan failed for "{{path}}": {{error}}` |
| Symlink cycle detected | warning | `FileTreeBrowser: symlink cycle detected at "{{path}}", skipping` |
| Settings changed | debug | `FileTreeBrowser: settings changed, triggering full resync` |
| Git status refresh | debug | `FileTreeBrowser: git status refresh (debounced)` |

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Expand/collapse transitions are instant (no rotation animation on disclosure indicator) |
| Increase Contrast | Selection highlight and icon colors use higher-contrast values |
| Differentiate Without Color | Distinct SF Symbol shapes already differentiate file types without relying on color (icon-shape-not-color) |
| VoiceOver | Row labels include entry name, type, and git status; expand/collapse state announced |

## Platform Notes

- **SwiftUI**: Use `List` with `OutlineGroup` and `.listStyle(.sidebar)`. Model `FileTreeNode` as an `ObservableObject` with `@Published children: [FileTreeNode]?` (nil = not yet loaded, empty = loaded but empty). Load children on `OutlineGroup`'s `children` keypath access. Git status fetched via a separate provider running on a background `DispatchQueue`. Parallel scanning via `OperationQueue` with `maxConcurrentOperationCount` set to `maxScanWorkers`. Ignore patterns evaluated using `fnmatch()` from Darwin. Icons via `Image(systemName:)` with `.foregroundStyle()` for theming. Tooltips via `.help()` modifier (macOS).
- **visionOS**: Same SwiftUI implementation as macOS. List renders in a volume or window with standard sidebar appearance. No platform-specific adjustments beyond standard visionOS adaptations.
- **iOS**: Same SwiftUI implementation. Sidebar presented in `NavigationSplitView` sidebar column. Disclosure indicators use standard iOS chevron style.

## Design Decisions

_None yet -- decisions made during implementation should be recorded here._

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

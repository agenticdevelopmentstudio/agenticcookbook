<!-- leaf: ingredients-ui/panels-file-tree-browser · source: ingredients/ui/panels/file-tree-browser.md -->

**Rules** (cite as `ingredients-ui/panels-file-tree-browser#<slug>`):

- `outline-group-hierarchy` MUST
- `lazy-child-loading` MUST
- `parallel-top-level-scan` MUST
- `sidebar-list-style` MUST
- `dirs-first-alpha-sort` MUST
- `fnmatch-ignore-patterns` MUST
- `show-dotfiles` MUST
- `hide-ds-store` MUST
- `package-dir-display` MUST
- `single-file-selection` MUST
- `git-status-badge` MUST
- `git-debounce-refresh` MUST
- `git-background-fetch` MUST
- `sync-status-bar` MUST
- `delegate-directory-sync` MUST
- `row-accessible-label` MUST
- `git-badge-accessible` MUST
- `keyboard-tree-nav` MUST
- `voiceover-row-announce` MUST
- `icon-shape-not-color` MUST
- `per-project-settings` MUST
- `setting-change-resync` MUST

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

- **git-status-badge**: Each file row MUST display a git status badge when the file has a git status. The badge MUST be right-aligned, use a monospaced font, and be colored per status type. Badge rendering MUST delegate to git-status-indicator.md.
- **git-debounce-refresh**: Git status MUST refresh with a 0.5-second debounce after file changes to prevent thrashing.
- **git-background-fetch**: Git status MUST be fetched on a background queue and MUST NOT block the main thread.

### Status bar integration

- **sync-status-bar**: During directory sync operations, a status bar overlay MUST be shown. Display MUST delegate to status-bar.md.

### Directory sync lifecycle

- **delegate-directory-sync**: File system monitoring and sync behavior MUST delegate to directory-sync.md.

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

## Accessibility

- **row-accessible-label**: Each row MUST have an accessibility label that includes the entry name and type (file or directory).
- **git-badge-accessible**: Git status badges MUST have accessibility labels with the full status name (e.g., "Modified") rather than the single character.
- **keyboard-tree-nav**: The tree MUST be navigable via keyboard — arrow keys to move between rows, Right arrow to expand, Left arrow to collapse.
- **voiceover-row-announce**: VoiceOver MUST announce the entry name, type, and git status (if any) when a row gains focus.
- **icon-shape-not-color**: Color MUST NOT be the sole differentiator for file type icons — the distinct SF Symbol shapes provide differentiation without color.

## Configuration

This ingredient has no configurable options.

## Project Settings

| Setting | Type | Default | Constraints | Description |
|---------|------|---------|-------------|-------------|
| `ignorePatterns` | `[String]` | `[]` | POSIX fnmatch() wildcards | Wildcard patterns to hide from the tree |
| `maxScanWorkers` | `Int` | `3` | 1-8 | Maximum parallel scan concurrency for top-level directory scanning |

- **per-project-settings**: Both settings MUST be configured per-project.
- **setting-change-resync**: Changing either setting MUST trigger a full resync of the file tree.

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

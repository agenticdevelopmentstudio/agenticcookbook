---
id: 7264C7B6-593E-4ED9-8974-F5EA5E4DB123
title: "Workspace Browser"
domain: agenticdevelopercookbook://ingredients/ui/windows/workspace-browser
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Sidebar of project and directory entries with auto-discovered projects, a detail pane with welcome empty state, context menus, and a sync indicator"
platforms:
  - macos
  - swift
  - web
tags:
  - browser
  - sidebar
  - ui
  - workspace
depends-on:
  - agenticdevelopercookbook://ingredients/ui/components/empty-state
related:
  - agenticdevelopercookbook://ingredients/ui/windows/workspace-document
  - agenticdevelopercookbook://recipes/ui/windows/workspace-window
  - agenticdevelopercookbook://recipes/infrastructure/directory-sync
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Workspace Browser

## Overview

The sidebar-and-detail UI for browsing a workspace of projects. A sidebar lists project entries and directory entries (each directory expands to show auto-discovered projects), a detail pane shows the selected entry or a welcome empty state, context menus remove entries, and a sync progress indicator appears while any directory is syncing. This ingredient owns presentation and interaction only; the persisted workspace data and directory-watching pool are the Workspace Document ingredient.

### Terminology

| Term | Definition |
|------|-----------|
| Workspace | A `.catnip-workspace` package that groups multiple project and directory references into a single browsable window |
| Entry | A reference to either a project file (`.catnip-proj`) or a directory to scan for projects |
| Project entry | An entry of type `.project` that directly references a `.catnip-proj` package |
| Directory entry | An entry of type `.directory` that references a folder scanned for `.catnip-proj` packages |
| Discovered project | A `.catnip-proj` package automatically found inside a watched directory entry |
| Sidebar proportion | The fractional width of the sidebar relative to the total window width (default 0.3) |
| Workspace document | The `.catnip-workspace` package containing `workspace.db` (SQLite) |
| Self-referential loop | The condition where a workspace's own `.catnip-workspace` package would be added as an entry |

## Behavioral Requirements

### Sidebar

- **two-section-sidebar**: The sidebar MUST display two sections: "Projects" (top) and "Directories" (bottom).
- **project-row-display**: The "Projects" section MUST list all entries of type `.project`. Each row MUST display a package icon (`shippingbox.fill`, orange) and the project name, with the file path shown as secondary text.
- **directory-disclosure-group**: The "Directories" section MUST list all entries of type `.directory`. Each directory entry MUST render as a `DisclosureGroup` that expands to show auto-discovered `.catnip-proj` packages within that directory.
- **directory-row-icon**: Each directory entry row MUST display a folder icon (`folder.fill`) and the directory name.
- **discovered-project-row**: Discovered projects within a directory `DisclosureGroup` MUST display a package icon (`shippingbox.fill`, orange) and the project name.
- **double-click-open**: Double-tapping (or double-clicking) a project entry or a discovered project MUST open that project via `NSDocumentController.shared.openDocument(withContentsOf:display:)`.
- **sync-progress-indicator**: A sync progress indicator MUST be displayed at the bottom of the sidebar when any directory coordinator is syncing. Display MUST follow the pattern in [directory-sync.md](../../../recipes/infrastructure/directory-sync.md) (aggregated `isSyncing` state).

### Context Menus

- **project-context-menu**: Each project entry MUST have a context menu with the following items:
  - "Open Project" — opens the project (same behavior as double-tap, double-click-open)
  - "Remove from Workspace" — removes the entry from the workspace document
- **directory-context-menu**: Each directory entry MUST have a context menu with the following item:
  - "Remove from Workspace" — removes the entry and its associated coordinator from the workspace

### Detail Pane

- **detail-pane-metadata**: When an entry is selected in the sidebar, the detail pane MUST display an entry detail view showing metadata or project information for the selected entry.
- **welcome-empty-state**: When no entry is selected, the detail pane MUST display an empty-state/welcome view as described in [empty-state.md](../components/empty-state.md), with the following action buttons:
  - "Add Directory" — opens a directory picker to add a new directory entry
  - "Add Project" — opens a file picker (filtered to `.catnip-proj`) to add a new project entry

## Appearance

```
+-------------------------------------------------------+
| Workspace: MyWorkspace                                |
+------------------+------------------------------------+
|                  |                                    |
| PROJECTS         |                                    |
|  [pkg] App.catnip|    Entry Detail View               |
|  [pkg] Lib.catnip|    or                              |
|                  |    Empty State / Welcome            |
| DIRECTORIES      |    ┌─────────────────────┐         |
|  [dir] ~/Code    |    │ [icon]              │         |
|    [pkg] Found1  |    │ Welcome to Workspace│         |
|    [pkg] Found2  |    │                     │         |
|  [dir] ~/Plugins |    │ [Add Directory]     │         |
|    [pkg] Found3  |    │ [Add Project]       │         |
|                  |    └─────────────────────┘         |
|                  |                                    |
+--[SyncProgressBar]+------------------------------------+
```

- **Layout**: `HSplitView` — sidebar (left), detail pane (right)
- **Sidebar width**: Proportional, default 0.3 of window width, user-adjustable via split divider
- **Section headers**: "Projects" and "Directories", uppercase, secondary color, small font weight
- **Project row**: Package icon (`shippingbox.fill`, orange) + project name (primary text) + path (secondary text, truncated)
- **Directory row**: Folder icon (`folder.fill`, accent) + directory name
- **Discovered project row**: Package icon (`shippingbox.fill`, orange) + project name, indented within disclosure group
- **Sync indicator**: `SyncProgressBar` at the bottom of the sidebar, visible only when syncing
- **Detail pane background**: Standard window background
- **Empty state**: Centered per [empty-state.md](../components/empty-state.md) with folder icon, welcome heading, and action buttons

## States

| State | Behavior |
|-------|----------|
| No entries | Sidebar shows empty sections, detail pane shows welcome empty state with add buttons (welcome-empty-state) |
| Entries present, none selected | Sidebar lists entries, detail pane shows welcome empty state (welcome-empty-state) |
| Entry selected | Sidebar highlights selection, detail pane shows entry detail (detail-pane-metadata) |
| Directory entry expanded | DisclosureGroup open, discovered projects listed (directory-disclosure-group) |
| Directory entry collapsed | DisclosureGroup closed, discovered projects hidden |
| Syncing | SyncProgressBar visible at sidebar bottom (sync-progress-indicator), `isSyncing` true |
| Sync complete | SyncProgressBar hidden, discovered projects up to date |
| Project opened | Project window opens via NSDocumentController, workspace window remains |

## Accessibility

- **keyboard-sidebar-nav**: The sidebar MUST be navigable via keyboard — arrow keys to move between entries, Return/Space to select, Right arrow to expand disclosure groups, Left arrow to collapse.
- **project-row-label**: Each project entry row MUST have an accessibility label that includes the project name and "project" role.
- **directory-row-label**: Each directory entry row MUST have an accessibility label that includes the directory name and "directory" role.
- **discovered-row-label**: Discovered project rows MUST have accessibility labels that include the project name and "discovered project" role.
- **sync-voiceover-announce**: The sync progress indicator MUST be announced by VoiceOver when its visibility changes (e.g., "Syncing directories" when it appears, "Sync complete" when it disappears).
- **context-menu-labels**: Context menu items MUST have descriptive accessibility labels matching their visible text.
- **tab-focus-transfer**: Tab key MUST move focus between the sidebar and detail pane.
- **empty-state-accessible**: The empty-state action buttons MUST be accessible per [empty-state.md](../components/empty-state.md) heading-first-announce through decorative-icon.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| ws-005 | two-section-sidebar | Workspace has 2 project entries and 1 directory entry | Sidebar shows "Projects" section with 2 rows and "Directories" section with 1 row |
| ws-006 | project-row-display | Project entry named "MyApp" at `/path/to/MyApp.catnip-proj` | Row shows orange package icon, "MyApp", and path as secondary text |
| ws-007 | directory-disclosure-group | Directory entry containing 2 `.catnip-proj` packages | DisclosureGroup expands to show 2 discovered project rows |
| ws-008 | double-click-open | Double-click a project entry | Project opens via NSDocumentController |
| ws-009 | double-click-open | Double-click a discovered project within a directory group | Project opens via NSDocumentController |
| ws-010 | sync-progress-indicator | 1 of 2 directory coordinators is syncing | SyncProgressBar visible at sidebar bottom |
| ws-011 | sync-progress-indicator | All coordinators finish syncing | SyncProgressBar hidden |
| ws-012 | project-context-menu | Right-click a project entry | Context menu shows "Open Project" and "Remove from Workspace" |
| ws-013 | directory-context-menu | Right-click a directory entry | Context menu shows "Remove from Workspace" |
| ws-014 | detail-pane-metadata | Select a project entry in sidebar | Detail pane shows project metadata/info |
| ws-015 | welcome-empty-state | No entry selected | Detail pane shows empty state with "Add Directory" and "Add Project" buttons |
| ws-016 | welcome-empty-state | Click "Add Directory" in empty state | Directory picker opens |
| ws-017 | welcome-empty-state | Click "Add Project" in empty state | File picker opens, filtered to .catnip-proj |
| ws-029 | keyboard-sidebar-nav | Focus sidebar, press Down arrow | Selection moves to next entry |
| ws-030 | keyboard-sidebar-nav | Focus on collapsed directory entry, press Right arrow | DisclosureGroup expands |
| ws-031 | tab-focus-transfer | Press Tab from sidebar | Focus moves to detail pane |

## Edge Cases

- **Empty workspace (no entries)**: Both sidebar sections show empty. Detail pane shows welcome empty state with add buttons. The window MUST NOT crash or display broken layout.
- **Directory entry points to non-existent path**: Entry SHOULD display with a warning indicator (e.g., exclamation mark badge). Coordinator SHOULD NOT be created for a missing path. Entry SHOULD remain in the list to allow the user to remove it.
- **Project entry points to non-existent .catnip-proj**: Entry SHOULD display with a warning indicator. Double-tap SHOULD show an error rather than crash.
- **Very long project/directory name**: Sidebar rows SHOULD truncate with ellipsis. Full path shown in tooltip.
- **Many entries (50+)**: Sidebar MUST scroll. Performance MUST remain acceptable with lazy list rendering.
- **Directory entry discovers zero projects**: DisclosureGroup expands but shows no children. SHOULD display a subtle "No projects found" message within the group.

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `projectIcon` | symbol | `shippingbox.fill` (orange) | Icon for project and discovered-project rows |
| `directoryIcon` | symbol | `folder.fill` (accent) | Icon for directory rows |
| `showPathTooltip` | Bool | `true` | Show the full path in a tooltip when a row is truncated |

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Disclosure group expand/collapse transitions are instant (no animation) |
| Reduce Transparency | Sidebar and detail pane use opaque backgrounds |
| Increase Contrast | Section headers, selection highlights, and icon colors use higher-contrast values |
| VoiceOver | Entry rows announce name, type, and status; disclosure state announced on directory entries; sync progress announced on visibility change; context menu items announced |

## Logging

Subsystem: `{{bundle_id}}` | Category: `WorkspaceWindow`

The window-level events are emitted by the Workspace Window recipe through this ingredient's category.

| Event | Level | Message |
|-------|-------|---------|
| Window opened | debug | `WorkspaceWindow: opened "{{workspacePath}}"` |
| Window closed | debug | `WorkspaceWindow: closed "{{workspacePath}}"` |
| Frame autosave set | debug | `WorkspaceWindow: autosave name "{{hashedName}}"` |
| Sidebar proportion changed | debug | `WorkspaceWindow: sidebar proportion changed to {{value}}` |
| Entry selected | debug | `WorkspaceWindow: selected entry "{{name}}" ({{entryType}})` |
| Project opened | info | `WorkspaceWindow: opening project "{{path}}"` |
| Project open failed | error | `WorkspaceWindow: failed to open project "{{path}}": {{error}}` |
| Empty state displayed | debug | `WorkspaceWindow: showing welcome empty state` |
| Add directory picker shown | debug | `WorkspaceWindow: showing directory picker` |
| Add project picker shown | debug | `WorkspaceWindow: showing project picker` |
| Non-existent entry path | warning | `WorkspaceWindow: entry "{{path}}" does not exist on disk` |

## Platform Notes

- **SwiftUI (macOS)**: Use `HSplitView` (or `NavigationSplitView` with `.navigationSplitViewStyle(.balanced)`) for the two-pane layout. Sidebar sections use `Section` headers ("Projects", "Directories"). Project rows use `Label` with `Image(systemName: "shippingbox.fill").foregroundStyle(.orange)`. Directory entries use `DisclosureGroup`. Double-click handled via `.onTapGesture(count: 2)` or `List` selection with `onSubmit`. Context menus via `.contextMenu { }`. Open projects via `NSDocumentController.shared.openDocument(withContentsOf:display:completionHandler:)`. Sync indicator as an overlay or bottom bar within the sidebar column.
- **visionOS**: Same SwiftUI implementation as macOS. `HSplitView` / `NavigationSplitView` adapts to visionOS layout conventions. Double-tap replaces double-click for project opening. Context menus triggered via long press or secondary gesture. `NSDocumentController` is not available on visionOS — project opening must use an alternative mechanism (e.g., custom document handling or `UIDocumentBrowserViewController` equivalent). The `SyncProgressBar` renders identically.
- **Compose**: Render the sidebar as a `LazyColumn` with section headers and expandable directory rows; the detail pane is a sibling `Box`. Context menus via `DropdownMenu` on long press or right click.
- **React/Web**: Render the sidebar as a tree list with expandable directory rows (`aria-expanded`), and the detail pane as a sibling region. Context menus via a menu component triggered by right click or the keyboard menu key.

## Design Decisions

**Decision**: Split the workspace window into a presentation ingredient (browser) and a data ingredient (document).
**Rationale**: Presentation can change (sidebar, tree, tabs) without touching the persisted package format or the directory-watching pool (design-for-deletion).
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [localization](agenticdevelopercookbook://guidelines/implementing/internationalization/localization) | partial | Localization |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Workspace Window recipe |

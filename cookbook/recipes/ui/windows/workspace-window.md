---
id: 3b83a80f-d170-4ef6-a608-81f3a1476679
title: "Workspace Window"
domain: agenticdevelopercookbook://recipes/ui/windows/workspace-window
type: recipe
version: 2.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Two-pane workspace browser window for managing multiple projects with auto-discovery of project packages"
platforms:
  - macos
  - swift
  - web
tags:
  - ui
  - window
  - workspace-window
ingredients:
  - agenticdevelopercookbook://ingredients/ui/windows/workspace-browser
  - agenticdevelopercookbook://ingredients/ui/windows/workspace-document
  - agenticdevelopercookbook://ingredients/ui/components/empty-state
  - agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence
  - agenticdevelopercookbook://ingredients/infrastructure/logging
depends-on: []
related:
  - agenticdevelopercookbook://recipes/infrastructure/directory-sync
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Workspace Window

## Overview

A two-pane workspace browser window for managing multiple projects. A horizontal split holds the Workspace Browser (sidebar of projects and directories, detail pane or welcome state) and is backed by the Workspace Document, a `.catnip-workspace` package with a SQLite database and a pool of directory watchers that auto-discover `.catnip-proj` packages. The window persists its frame keyed by a hash of the workspace path and persists the sidebar proportion in the workspace document.

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Workspace Browser | `agenticdevelopercookbook://ingredients/ui/windows/workspace-browser` | Sidebar, detail pane, context menus, welcome state, sync indicator | Yes | Sidebar default 0.3 |
| Workspace Document | `agenticdevelopercookbook://ingredients/ui/windows/workspace-document` | Persisted entries, directory-watch pool, discovery, validation | Yes | Cache dir `cache-{entryID}` |
| Empty State | `agenticdevelopercookbook://ingredients/ui/components/empty-state` | Welcome view when no entry is selected | Yes | Actions: Add Directory, Add Project |
| Window Frame Persistence | `agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence` | Persists window position and size | Yes | Autosave name = hash of the workspace file path |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Window-level logging | Yes | Category `WorkspaceWindow` |

## Integration Requirements

- **hsplit-sidebar-detail**: The window MUST use an `HSplitView` with a sidebar on the left and a detail pane on the right.
- **persist-window-frame**: The window MUST persist its frame (position and size) between sessions using the window frame persistence mechanism described in [window-frame-persistence.md](../../../ingredients/infrastructure/window-frame-persistence.md). The autosave name MUST be derived from a hash of the workspace file path.
- **sidebar-default-30pct**: The sidebar proportion MUST default to `0.3` and MUST be persisted in the workspace document's `settings` table.
- **resizable-min-size**: The window MUST be resizable with a minimum size sufficient to display the sidebar and detail pane without clipping content.
- **browser-bound-to-document**: The Workspace Browser MUST render exclusively from the Workspace Document's entries, discovered projects, and aggregated `isSyncing` state, and MUST NOT read the file system directly.
- **edits-flow-to-document**: Add and remove actions in the browser (context menus, welcome-state buttons) MUST be applied through the Workspace Document so that validation (duplicate and self-referential rejection) and `syncEntries` run before the sidebar updates.
- **sidebar-proportion-via-document**: The sidebar proportion MUST be read from and written to the Workspace Document's `settings` table, not to window-level storage.
- **frame-key-from-path**: The frame autosave name MUST be a hash of the workspace file path so each workspace window restores independently.
- **window-events-logged**: Window open, close, autosave-name, and sidebar-proportion events MUST use the `logging` ingredient with category `WorkspaceWindow`.

## Layout

```
+-------------------------------------------------------+
| Workspace: MyWorkspace                  (window frame)|
+------------------+------------------------------------+
| Workspace Browser| Workspace Browser detail pane      |
| sidebar (0.3)    | or Empty State (welcome)           |
| PROJECTS         |                                    |
| DIRECTORIES      |                                    |
|  (discovered)    |                                    |
+--[SyncProgressBar]+-----------------------------------+
        ^ all data: Workspace Document (workspace.db)
```

The window supplies the split, frame, and sidebar proportion; the browser fills both panes; the document supplies every entry. See the Workspace Browser ingredient's Appearance section for the full pane layout.

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Entries and discovered projects | Workspace Document | Workspace Browser sidebar | one-way | Observable document model |
| Aggregated `isSyncing` | Workspace Document (directory-watch pool) | Sync indicator in the browser | one-way | Any coordinator syncing sets it true |
| Add and remove commands | Workspace Browser | Workspace Document | one-way | Validated, then `syncEntries` reconciles the pool |
| Sidebar proportion | Window split divider | Workspace Document `settings` table | two-way | Persisted on change, restored on open |
| Window frame | Window | Window Frame Persistence | two-way | Autosave name from workspace path hash |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| ws-001 | hsplit-sidebar-detail | Open a workspace window | HSplitView renders with sidebar (left) and detail pane (right) |
| ws-002 | persist-window-frame | Open workspace, move window to (100, 200), close, reopen | Window appears at (100, 200) |
| ws-003 | sidebar-default-30pct | Open workspace, do not adjust sidebar | Sidebar occupies approximately 30% of window width |
| ws-004 | sidebar-default-30pct | Adjust sidebar proportion to 0.4, close workspace, reopen | Sidebar proportion restored to 0.4 |
| ws-032 | edits-flow-to-document, prevent-duplicate-entry | Use the welcome-state "Add Directory" button to add a path that already exists | Add is rejected by the document; sidebar does not change |
| ws-033 | browser-bound-to-document, auto-discover-projects | A new `.catnip-proj` appears in a watched directory | `onDiscoveryChanged` updates the document and the sidebar shows the new discovered project |
| ws-034 | sidebar-proportion-via-document | Drag the divider, close and reopen the workspace | Proportion is restored from the document's `settings` table |
| ws-035 | frame-key-from-path, window-events-logged | Open two different workspaces and move each window | Each window restores to its own frame; logs show distinct autosave names |

## Edge Cases

- **All entries removed**: Returns to empty workspace state. All coordinators stopped.
- **Sidebar proportion at extremes**: If the user drags the split divider to an extreme (< 0.15 or > 0.85), the proportion SHOULD be clamped to maintain usability.

## Platform Notes

- **SwiftUI (macOS)**: Frame autosave via the `WindowAccessor` pattern from [window-frame-persistence.md](../../../ingredients/infrastructure/window-frame-persistence.md) with the autosave name set to a SHA256 hash prefix of the workspace path. Compose the Workspace Browser inside an `HSplitView` (or `NavigationSplitView`) and bind it to the Workspace Document model.
- **SwiftUI (visionOS)**: Frame persistence may not apply in the same way; window placement is managed by the system. The composition is otherwise identical to macOS.
- **Compose**: Use a `Window` with `rememberWindowState` keyed by a hash of the workspace path; bind the browser to a document view model.
- **React/Web**: Persist window layout in `localStorage` keyed by a hash of the workspace path; bind the browser to a document store.

## Design Decisions

**Decision**: Compose the window from a browser ingredient and a document ingredient, plus empty state, frame persistence, and logging.
**Rationale**: Presentation, persistence, and window behavior each have a single owner, so a different UI can reuse the same workspace document.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |
| [error-responses](agenticdevelopercookbook://guidelines/implementing/networking/error-responses) | partial | Best Practices |

> Status is `partial`: this recipe specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-10-04 | Mike Fullerton | Restructured into recipe shape: composes workspace-browser and workspace-document |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

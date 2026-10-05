---
id: 31f97683-8d2e-4203-a155-48cebc1bfb13
title: "Settings Window"
domain: agenticdevelopercookbook://recipes/ui/windows/settings-window
type: recipe
version: 2.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Standard desktop settings/preferences window with sidebar categories and immediate-apply controls"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
  - windows
tags:
  - settings-window
  - ui
  - window
ingredients:
  - agenticdevelopercookbook://ingredients/ui/windows/settings-category-browser
  - agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence
  - agenticdevelopercookbook://ingredients/infrastructure/settings-keys
  - agenticdevelopercookbook://ingredients/infrastructure/logging
  - agenticdevelopercookbook://ingredients/ui/components/empty-state
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Settings Window

## Overview

The standard desktop settings or preferences window. It opens from the conventional menu location through the platform keyboard shortcut, is single-instance and non-modal, remembers its frame, and never reopens on launch. The Settings Category Browser supplies the sidebar and content panel; window frame persistence, logging, and the settings-keys registry are composed alongside it. Changes apply immediately, with no save or apply button.

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Settings Category Browser | `agenticdevelopercookbook://ingredients/ui/windows/settings-category-browser` | Sidebar categories, content panel, immediate apply, persistence abstraction | Yes | Layout variant per app; first category selected by default |
| Window Frame Persistence | `agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence` | Remembers window size and position between sessions | Yes | Minimum size 500x400pt |
| Settings Keys | `agenticdevelopercookbook://ingredients/infrastructure/settings-keys` | Central registry of setting keys | Yes | Keys in an enum or struct of static constants |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Logger for window-level events | Yes | Category `SettingsWindow` |
| Empty State | `agenticdevelopercookbook://ingredients/ui/components/empty-state` | Message shown when no categories are defined | No | Strings `settings.no_categories`, `settings.no_settings` |

## Integration Requirements

- **platform-keyboard-open**: The window MUST open via the platform-standard keyboard shortcut:
  - macOS: `⌘,` from the app menu (app name menu), labeled "Settings…" (macOS 13+) or "Preferences…" (older)
  - Windows: `Ctrl+,` from the File menu, labeled "Settings"
  - Linux: from the Edit or app menu, labeled "Preferences"
- **single-instance-enforce**: The app MUST enforce single-instance — if the shortcut is triggered while the window is open, the existing window MUST be brought to front. A second instance MUST NOT be created.
- **non-modal-window**: The window MUST be non-modal — it MUST NOT block interaction with other app windows.
- **no-auto-reopen**: The window MUST NOT reopen automatically on app launch, even if it was open when the app was last quit.
- **persist-frame-position**: The window MUST remember its size and position between sessions using the platform's standard frame autosave mechanism.
- **resizable-min-size**: The window MUST be resizable with a minimum size of 500×400pt.
- **centralized-keys**: Settings keys MUST be centralized in an enum or struct of static constants (e.g., `SettingsKeys.general.startupBehavior`). This prevents key duplication and typos across the app.
- **per-document-settings**: Apps with documents or projects SHOULD support per-document settings in addition to app-wide settings. Per-document settings MUST be presented as a sheet (not mixed into the main settings window), typically triggered by a toolbar gear button.
- **browser-fills-window**: The Settings Category Browser MUST fill the window content area, and the window MUST NOT add controls outside it, so the window stays free of Apply or Save buttons.
- **keys-through-registry**: The browser's persistence layer MUST read and write setting keys declared through the `settings-keys` ingredient.
- **frame-through-ingredient**: Frame saving and restoring MUST be performed by the `window-frame-persistence` ingredient, keyed to the settings window, and MUST NOT depend on any category selection.
- **log-window-events**: Window open, front, close, and frame-saved events MUST use the `logging` ingredient with category `SettingsWindow`.

## Layout

```
 App menu > Settings...  (platform shortcut)
        |
        v
┌──────────────────────────────────────────────┐
│ Settings                         (min 500×400)│
├────────────┬─────────────────────────────────┤
│ Sidebar    │  Content panel                  │
│ General    │  Setting Label         [control]│
│ Appearance │  Setting Label         [control]│
│ Advanced   │  Setting Label         [control]│
├────────────┴─────────────────────────────────┤
```

The sidebar and content panel are the Settings Category Browser; the title bar, frame, and instance behavior belong to the window. The sidebar and content layout variants are defined by the browser's Appearance section.

### Composed states

| State | Behavior |
|-------|----------|
| No window open | Menu item and keyboard shortcut are enabled |
| Window open, shortcut triggered | Existing window brought to front (single-instance-enforce) |
| Window resized | Frame saved automatically for next open (persist-frame-position) |
| App quit with window open | Window does not reopen on next launch (no-auto-reopen) |

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Setting values | Settings Category Browser controls | Persistence layer, rest of the app | two-way | Written immediately through settings-keys constants |
| Window frame | Window | Window Frame Persistence | two-way | Platform frame autosave |
| Window instance | Window controller | Menu item and shortcut handler | one-way | Existing instance is brought to front instead of creating another |
| Selected category | Settings Category Browser | Content panel | one-way | Not persisted across launches |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| settings-001 | single-instance-enforce | Open settings window, trigger shortcut again | Window count remains 1, existing window is key/front |
| settings-002 | no-auto-reopen | Open settings, quit app, relaunch | Settings window is not visible after relaunch |
| settings-003 | persist-frame-position | Open settings, resize to 600×500 at (100,200), close, reopen | Window opens at 600×500 at (100,200) |
| settings-007 | resizable-min-size | Attempt to resize window below 500×400 | Window does not shrink below minimum |
| settings-010 | log-window-events, single-instance-enforce | Trigger the shortcut while the window is open | Log contains `SettingsWindow: already open, brought to front` |
| settings-011 | keys-through-registry, immediate-apply | Toggle a setting | The value is written under the key declared in the settings-keys registry |
| settings-012 | browser-fills-window | Inspect the open window | No Apply or Save control is present anywhere in the window |

## Edge Cases

- **Window open while app quits**: The window MUST NOT reopen on next launch, and the saved frame MUST still be available if the user opens it manually (no-auto-reopen, persist-frame-position).
- **Frame restored off-screen**: If the saved frame is on a display that is no longer attached, the window SHOULD open on a visible display at its saved size, honoring the minimum size.
- **Shortcut during category switch**: Triggering the shortcut while the content panel is updating MUST bring the existing window to front without resetting the selected category.
- **Per-document settings open**: The per-document settings sheet MUST NOT be reachable from, or merged into, this window; opening the main settings window MUST NOT dismiss the sheet.

## Platform Notes

- **SwiftUI (macOS)**: Register `⌘,` via the `Settings` scene (preferred) or the `.commands` modifier with `CommandGroup(replacing: .appSettings)`. For single-instance enforcement, use a `Window` scene with `defaultPosition` and `handlesExternalEvents`. Frame autosave via `SceneStorage` or `WindowGroup(id:)`. For per-document settings, present `ProjectSettingsView` as `.sheet(isPresented:)` from a toolbar gear button.
- **Compose (Windows)**: Use `Window` with `rememberWindowState()` for position and size persistence. Register `Ctrl+,` via `MenuBar` and a keyboard shortcut handler.
- **React/Electron (Desktop)**: Use a `BrowserWindow` with `show: false` initially. Track the instance to prevent duplicates. Register the shortcut via `globalShortcut` or a menu accelerator.

## Design Decisions

**Decision**: Compose the window from a dedicated category-browser ingredient plus frame persistence, settings keys, and logging, rather than one monolithic window spec.
**Rationale**: The browser is reusable inside other hosts (sheets, inspectors); window-level concerns stay separate.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |
| [lifecycle-patterns](agenticdevelopercookbook://guidelines/planning/code-quality/lifecycle-patterns) | partial | Best Practices |

> Status is `partial`: this recipe specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-10-04 | Mike Fullerton | Restructured into recipe shape: composes settings-category-browser with frame persistence, settings keys, and logging |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

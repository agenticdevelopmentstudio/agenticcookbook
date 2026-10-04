---
id: 31f97683-8d2e-4203-a155-48cebc1bfb13
title: "Settings Window"
domain: agenticdevelopercookbook://recipes/ui/windows/settings-window
type: recipe
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-03-27
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
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# Settings Window

## Overview

A standard desktop application settings/preferences window. Opens from the conventional menu location via platform-standard keyboard shortcut. Displays setting categories in a sidebar with the corresponding settings panel on the right. Changes apply immediately — no save/apply button.

## Terminology

| Term | Definition |
|------|-----------|
| Category | A named group of related settings displayed in the sidebar |
| Content panel | The right-side area showing settings for the selected category |
| Frame autosave | Platform mechanism for persisting window position and size between sessions |

## Behavioral Requirements

- **platform-keyboard-open**: The window MUST open via the platform-standard keyboard shortcut:
  - macOS: `⌘,` from the app menu (app name menu), labeled "Settings…" (macOS 13+) or "Preferences…" (older)
  - Windows: `Ctrl+,` from the File menu, labeled "Settings"
  - Linux: from the Edit or app menu, labeled "Preferences"
- **single-instance-enforce**: The app MUST enforce single-instance — if the shortcut is triggered while the window is open, the existing window MUST be brought to front. A second instance MUST NOT be created.
- **non-modal-window**: The window MUST be non-modal — it MUST NOT block interaction with other app windows.
- **no-auto-reopen**: The window MUST NOT reopen automatically on app launch, even if it was open when the app was last quit.
- **persist-frame-position**: The window MUST remember its size and position between sessions using the platform's standard frame autosave mechanism.
- **resizable-min-size**: The window MUST be resizable with a minimum size of 500×400pt.
- **immediate-apply**: Setting changes MUST take effect immediately when the user interacts with the control. There MUST NOT be an "Apply" or "Save" button.
- **sidebar-category-list**: The sidebar MUST display a vertical list of category names. The first category MUST be selected by default.
- **category-content-update**: Selecting a category MUST update the content panel to show that category's settings.
- **content-vertical-scroll**: The content panel MUST scroll vertically if its content exceeds the panel height.
- **abstract-persistence**: Settings MUST be read from and written to a persistence layer. The storage backend SHOULD be abstracted behind an interface so it can be swapped without changing consumers. Common backends:
  - macOS/iOS: `UserDefaults` / `@AppStorage` (default), or SQLite for apps that need migration-safe structured storage
  - Windows: Registry or app config file
  - Web/Electron: `localStorage` or `electron-store`
  - Note: apps MAY migrate from one backend to another (e.g., UserDefaults → SQLite) — see `settings-keys.md` for key preservation during migration
- **centralized-keys**: Settings keys MUST be centralized in an enum or struct of static constants (e.g., `SettingsKeys.general.startupBehavior`). This prevents key duplication and typos across the app.
- **per-document-settings**: Apps with documents or projects SHOULD support per-document settings in addition to app-wide settings. Per-document settings MUST be presented as a sheet (not mixed into the main settings window), typically triggered by a toolbar gear button.
- **form-section-layout**: The content panel SHOULD use `Form` with `Section` blocks for grouping related settings with clear section headers.

## Appearance

```
┌──────────────────────────────────────────────┐
│ Settings                                     │
├────────────┬─────────────────────────────────┤
│            │                                 │
│ General    │  Setting Label         [control]│
│ Appearance │  Setting Label         [control]│
│ Advanced   │  Setting Label         [control]│
│            │                                 │
│            │                                 │
│            │                                 │
│            │                                 │
├────────────┴─────────────────────────────────┤
```

- **Layout variant — Sidebar** (default, for 4+ categories): Horizontal split view — sidebar on left, content panel on right
- **Layout variant — Tab bar** (for fewer categories or per platform convention): Horizontal tab bar at top, content panel below. Use when there are fewer than 5 categories or when the platform convention prefers tabs (e.g., macOS System Settings pre-Ventura). This is a **Design Decision** — document which variant is chosen.
- **Sidebar width**: Fixed or narrow resizable range (150–220pt)
- **Sidebar selection**: Platform-native selection highlight
- **Content layout**: Labeled rows — label on left, control on right. Group related settings with section headers.
- **Controls**: Native controls only — toggles, dropdowns/pickers, sliders, text fields, steppers
- **Category icons**: Optional — whether to show icons alongside category names is a **Design Decision** that MUST be approved by the user

## States

| State | Behavior |
|-------|----------|
| No window open | Menu item and keyboard shortcut are enabled |
| Window open, shortcut triggered | Existing window brought to front (single-instance-enforce) |
| Category selected | Content panel updates to show that category's settings (category-content-update) |
| Window resized | Frame saved automatically for next open (persist-frame-position) |
| App quit with window open | Window does not reopen on next launch (no-auto-reopen) |
| Setting changed | Change persisted and applied immediately (immediate-apply) |

## Accessibility

- **keyboard-sidebar-nav**: The sidebar list MUST be navigable via keyboard (arrow keys to move selection, Return/Space to confirm).
- **tab-focus-transfer**: Tab key MUST move focus between the sidebar and content panel controls.
- **control-accessible-labels**: All setting controls MUST have accessible labels.
- **announce-category-name**: VoiceOver/screen reader MUST announce the selected category name when selection changes.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| settings-001 | single-instance-enforce | Open settings window, trigger shortcut again | Window count remains 1, existing window is key/front |
| settings-002 | no-auto-reopen | Open settings, quit app, relaunch | Settings window is not visible after relaunch |
| settings-003 | persist-frame-position | Open settings, resize to 600×500 at (100,200), close, reopen | Window opens at 600×500 at (100,200) |
| settings-004 | immediate-apply | Toggle a boolean setting | Setting value in persistence layer matches new state immediately |
| settings-005 | sidebar-category-list | Open settings window | First category in list is selected, content panel shows its settings |
| settings-006 | category-content-update | Select second category | Content panel updates to show second category's settings |
| settings-007 | resizable-min-size | Attempt to resize window below 500×400 | Window does not shrink below minimum |
| settings-008 | keyboard-sidebar-nav | Focus sidebar, press Down arrow | Selection moves to next category |
| settings-009 | tab-focus-transfer | Press Tab from sidebar | Focus moves to first control in content panel |

## Edge Cases

- **No categories defined**: The window SHOULD display an empty state message rather than crashing.
- **Category with no settings**: The content panel SHOULD show a message like "No settings available" rather than a blank panel.
- **Extremely long category name**: Sidebar SHOULD truncate with ellipsis rather than expanding width.
- **Many settings in one category**: Content panel scrolls (content-vertical-scroll); performance SHOULD remain smooth with 50+ settings.
- **Rapid category switching**: Content panel MUST update without flicker or stale content.

## Logging

Subsystem: `{{bundle_id}}` | Category: `SettingsWindow`

| Event | Level | Message |
|-------|-------|---------|
| Window opened | debug | `SettingsWindow: opened` |
| Window brought to front | debug | `SettingsWindow: already open, brought to front` |
| Window closed | debug | `SettingsWindow: closed` |
| Category selected | debug | `SettingsWindow: selected category "{{name}}"` |
| Setting changed | debug | `SettingsWindow: changed "{{key}}" from "{{oldValue}}" to "{{newValue}}"` |
| Frame saved | debug | `SettingsWindow: frame saved ({{x}}, {{y}}, {{width}}×{{height}})` |

## Deep Linking

| Platform | URL Pattern | Behavior |
|----------|-------------|----------|
| Apple | `{{app_scheme}}://settings` or `{{app_scheme}}://settings/{{category}}` | Opens settings window, optionally navigates to a specific category |
| Windows | Command-line flag `--settings` or `--settings={{category}}` | Opens settings on launch |
| Web/Electron | `/settings` or `/settings/{{category}}` | Routes to settings view |

## Localization

| String Key | Default (en) | Context |
|-----------|-------------|---------|
| `settings.window_title` | Settings | Window title bar |
| `settings.no_categories` | No settings categories available | Empty state when no categories defined |
| `settings.no_settings` | No settings available | Empty state when a category has no settings |
| `settings.select_category` | Select a Category | Placeholder in detail panel before selection |

All category names and setting labels MUST also be localizable — they are app-specific and defined at implementation time.

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Sidebar selection change updates content panel instantly (no slide transition) |
| Reduce Transparency | Sidebar and content panel use opaque backgrounds |
| Increase Contrast | Sidebar selection highlight and control borders use higher-contrast colors |
| VoiceOver / TalkBack | Category list announces selection, setting labels and values announced, state changes announced |

## Privacy

- **Data collected**: User preferences (setting values only)
- **Storage**: Platform standard persistence (`UserDefaults`, registry, `localStorage`) — on-device only
- **Transmission**: None — settings do not leave the device
- **Retention**: Persisted until user changes or app is uninstalled

## Platform Notes

- **SwiftUI (macOS)**: Use `NavigationSplitView` with `.navigationSplitViewStyle(.balanced)`. Register `⌘,` via `Settings` scene (preferred) or `.commands` modifier with `CommandGroup(replacing: .appSettings)`. For single-instance enforcement, use `Window` scene with `defaultPosition` and `handlesExternalEvents`. Use `@AppStorage` with centralized `SettingsKeys` constants for binding settings. Use `Form { Section("Header") { ... } }` for content panel layout. Frame autosave via `SceneStorage` or `WindowGroup(id:)`. For per-document settings, present `ProjectSettingsView` as `.sheet(isPresented:)` from a toolbar gear button.
- **Compose (Windows)**: Use `Window` with `rememberWindowState()` for position/size persistence. Use a `Row` with a `LazyColumn` sidebar and content panel. Store settings in a preferences file. Register `Ctrl+,` via `MenuBar` and keyboard shortcut handler.
- **React/Electron (Desktop)**: Use a `BrowserWindow` with `show: false` initially. Track instance to prevent duplicates. Use CSS Grid or Flexbox for the split layout. Persist settings in `electron-store` or `localStorage`. Register shortcut via `globalShortcut` or menu accelerator.

## Design Decisions

_None yet — decisions made during implementation should be recorded here._

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

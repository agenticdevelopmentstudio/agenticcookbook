---
id: 4A047375-7F4F-4BCA-84A5-62A0F70FC5C9
title: "Settings Category Browser"
domain: agenticdevelopercookbook://ingredients/ui/windows/settings-category-browser
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Sidebar of setting categories with a scrollable content panel that applies changes immediately to an abstracted persistence layer"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
  - windows
tags:
  - settings
  - sidebar
  - ui
  - window
depends-on: []
related:
  - agenticdevelopercookbook://recipes/ui/windows/settings-window
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Settings Category Browser

## Overview

A sidebar-and-content browser for application settings. A vertical list of category names sits on the left; selecting one shows that category's settings on the right in a scrollable form. Changes apply immediately to a persistence layer, with no Apply or Save button. This ingredient owns the category list, content panel, immediate-apply behavior, and persistence abstraction. The window that hosts it (menu entry, single instance, frame persistence) is composed by the Settings Window recipe.

### Terminology

| Term | Definition |
|------|-----------|
| Category | A named group of related settings displayed in the sidebar |
| Content panel | The right-side area showing settings for the selected category |
| Frame autosave | Platform mechanism for persisting window position and size between sessions |

## Behavioral Requirements

- **immediate-apply**: Setting changes MUST take effect immediately when the user interacts with the control. There MUST NOT be an "Apply" or "Save" button.
- **sidebar-category-list**: The sidebar MUST display a vertical list of category names. The first category MUST be selected by default.
- **category-content-update**: Selecting a category MUST update the content panel to show that category's settings.
- **content-vertical-scroll**: The content panel MUST scroll vertically if its content exceeds the panel height.
- **abstract-persistence**: Settings MUST be read from and written to a persistence layer. The storage backend SHOULD be abstracted behind an interface so it can be swapped without changing consumers. Common backends:
  - macOS/iOS: `UserDefaults` / `@AppStorage` (default), or SQLite for apps that need migration-safe structured storage
  - Windows: Registry or app config file
  - Web/Electron: `localStorage` or `electron-store`
  - Note: apps MAY migrate from one backend to another (e.g., UserDefaults → SQLite) — see the `settings-keys` ingredient for key preservation during migration
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
| Category selected | Content panel updates to show that category's settings (category-content-update) |
| Setting changed | Change persisted and applied immediately (immediate-apply) |

## Accessibility

- **keyboard-sidebar-nav**: The sidebar list MUST be navigable via keyboard (arrow keys to move selection, Return/Space to confirm).
- **tab-focus-transfer**: Tab key MUST move focus between the sidebar and content panel controls.
- **control-accessible-labels**: All setting controls MUST have accessible labels.
- **announce-category-name**: VoiceOver/screen reader MUST announce the selected category name when selection changes.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| settings-004 | immediate-apply | Toggle a boolean setting | Setting value in persistence layer matches new state immediately |
| settings-005 | sidebar-category-list | Open settings window | First category in list is selected, content panel shows its settings |
| settings-006 | category-content-update | Select second category | Content panel updates to show second category's settings |
| settings-008 | keyboard-sidebar-nav | Focus sidebar, press Down arrow | Selection moves to next category |
| settings-009 | tab-focus-transfer | Press Tab from sidebar | Focus moves to first control in content panel |

## Edge Cases

- **No categories defined**: The window SHOULD display an empty state message rather than crashing.
- **Category with no settings**: The content panel SHOULD show a message like "No settings available" rather than a blank panel.
- **Extremely long category name**: Sidebar SHOULD truncate with ellipsis rather than expanding width.
- **Many settings in one category**: Content panel scrolls (content-vertical-scroll); performance SHOULD remain smooth with 50+ settings.
- **Rapid category switching**: Content panel MUST update without flicker or stale content.

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `layoutVariant` | enum (`sidebar`, `tabBar`) | `sidebar` | Sidebar for 4+ categories; tab bar for fewer than 5 categories or when platform convention prefers tabs |
| `sidebarWidth` | range (pt) | 150–220 | Fixed or narrow resizable sidebar width |
| `showCategoryIcons` | Bool | `false` | Whether icons appear beside category names; MUST be approved by the user |
| `initialCategory` | category id | first category | Category selected when the browser appears |
| `persistenceBackend` | interface | platform default | Storage backend behind the persistence abstraction (`UserDefaults`, SQLite, registry, `localStorage`) |

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
| `settings.select_category` | Select a Category | Prompt shown in the detail panel before selection |

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

## Platform Notes

- **SwiftUI (macOS)**: Use `NavigationSplitView` with `.navigationSplitViewStyle(.balanced)`. Use `@AppStorage` with centralized `SettingsKeys` constants for binding settings. Use `Form { Section("Header") { ... } }` for content panel layout.
- **Compose (Windows)**: Use a `Row` with a `LazyColumn` sidebar and content panel. Store settings in a preferences file.
- **React/Web**: Use CSS Grid or Flexbox for the split layout. Persist settings in `electron-store` or `localStorage`.

## Design Decisions

**Decision**: Layout variant (sidebar versus tab bar) is chosen per app and documented by the implementer.
**Rationale**: The Appearance section defines both variants and states that the choice is a Design Decision; the ingredient does not pick for the app.
**Approved**: pending

**Decision**: Category icons are optional and MUST be approved by the user before an implementation shows them.
**Rationale**: Whether to show icons alongside category names is a product decision, not a default.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [privacy](agenticdevelopercookbook://guidelines/implementing/security/privacy) | partial | Privacy |
| [localization](agenticdevelopercookbook://guidelines/implementing/internationalization/localization) | partial | Localization |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Settings Window recipe |

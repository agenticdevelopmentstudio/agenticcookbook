<!-- leaf: recipes-ui/windows-settings-window · source: recipes/ui/windows/settings-window.md -->

**Rules** (cite as `recipes-ui/windows-settings-window#<slug>`):

- `platform-keyboard-open` MUST
- `single-instance-enforce` MUST
- `non-modal-window` MUST
- `no-auto-reopen` MUST
- `persist-frame-position` MUST
- `resizable-min-size` MUST
- `immediate-apply` MUST
- `sidebar-category-list` MUST
- `category-content-update` MUST
- `content-vertical-scroll` MUST
- `abstract-persistence` MUST
- `centralized-keys` MUST
- `per-document-settings` MUST
- `form-section-layout` SHOULD
- `category-icons` MUST — Optional — whether to show icons alongside category names is a Design Decision that MUST be approved by the user
- `keyboard-sidebar-nav` MUST
- `tab-focus-transfer` MUST
- `control-accessible-labels` MUST
- `announce-category-name` MUST
- `names-setting-labels-also-localizable-they-app` MUST — All category names and setting labels MUST also be localizable — they are app-specific and defined at implementation …

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

## Accessibility

- **keyboard-sidebar-nav**: The sidebar list MUST be navigable via keyboard (arrow keys to move selection, Return/Space to confirm).
- **tab-focus-transfer**: Tab key MUST move focus between the sidebar and content panel controls.
- **control-accessible-labels**: All setting controls MUST have accessible labels.
- **announce-category-name**: VoiceOver/screen reader MUST announce the selected category name when selection changes.

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

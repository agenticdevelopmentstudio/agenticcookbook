---
id: 08f87323-4043-432f-8f29-936cfb4ed2e2
title: "Standalone Terminal Window"
domain: agenticdevelopercookbook://recipes/ui/windows/standalone-terminal-window
type: recipe
version: 2.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Standalone terminal window with session sidebar and independent session manager for non-project terminal use"
platforms:
  - macos
  - swift
  - windows
tags:
  - standalone-terminal-window
  - ui
  - window
ingredients:
  - agenticdevelopercookbook://ingredients/ui/windows/terminal-window-shell
  - agenticdevelopercookbook://ingredients/ui/panels/terminal-pane
  - agenticdevelopercookbook://ingredients/ui/components/color-profile
  - agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence
  - agenticdevelopercookbook://ingredients/infrastructure/logging
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Standalone Terminal Window

## Overview

The primary window for non-project terminal use. A `WindowGroup(id: "terminal")` scene hosts the Terminal Window Shell (session sidebar and terminal view with its own independent session manager), applies the active color profile, persists its frame under the autosave name `"terminal-window"`, and enforces a 600x400pt minimum size. It shares the terminal-pane ingredient with the project window's embedded terminal but shares no sessions with it.

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Terminal Window Shell | `agenticdevelopercookbook://ingredients/ui/windows/terminal-window-shell` | Sidebar and terminal split, per-window session manager, default session, terminate on close | Yes | Sidebar 150-200pt |
| Terminal Pane | `agenticdevelopercookbook://ingredients/ui/panels/terminal-pane` | Session list rows, terminal rendering, PTY lifecycle, empty state | Yes | Shared with the project window |
| Color Profile | `agenticdevelopercookbook://ingredients/ui/components/color-profile` | Active profile colors, font and cursor style; fallback to Solarized Dark | Yes | Active profile ID in global app storage |
| Window Frame Persistence | `agenticdevelopercookbook://ingredients/infrastructure/window-frame-persistence` | Persists window frame | Yes | Autosave name `"terminal-window"` |
| Logging | `agenticdevelopercookbook://ingredients/infrastructure/logging` | Window-level logging | Yes | Category `StandaloneTerminalWindow` (events defined by the shell) |

## Integration Requirements

### Window structure

- **window-group-terminal**: The window MUST use a `WindowGroup(id: "terminal")` scene declaration.
- **persist-window-frame**: The window frame MUST be persisted using the window-frame-persistence component (the `window-frame-persistence` ingredient). The autosave name MUST be `"terminal-window"`.
- **min-size-constraints**: The window MUST enforce minimum size constraints: minWidth 600pt, minHeight 400pt.

### Terminal view and profile

- **apply-active-profile**: The terminal view MUST apply the active color profile (colors, font, cursor style) from `TerminalProfile.activeProfile()`.
- **global-profile-storage**: The active profile ID MUST be read from `@AppStorage`. This is a global setting shared across all terminal windows.
- **profile-fallback-default**: If the stored active profile ID is invalid (not found among available profiles), the window MUST fall back to the first built-in profile (Solarized Dark), as specified in `color-profile` ingredient fallback-to-default.

### Relationship to project window

- **shared-terminal-spec**: The standalone terminal window and the project window's embedded terminal pane MUST share the same terminal-pane spec (`terminal-pane` ingredient) for all terminal behavior — PTY lifecycle, session management, terminal rendering, OSC handling, and session list display.

### Delegation to sub-components

- **delegate-session-list**: The session list sidebar MUST delegate to [terminal-pane.md](../../../ingredients/ui/panels/terminal-pane.md) sidebar-session-list through row-context-menu for session list behavior (row display, selection binding, add button, context menu).
- **delegate-terminal-view**: The terminal view MUST delegate to [terminal-pane.md](../../../ingredients/ui/panels/terminal-pane.md) nsview-representable through palette-color-structure for terminal rendering, reparenting, and profile application.
- **delegate-empty-state**: The empty state MUST delegate to [terminal-pane.md](../../../ingredients/ui/panels/terminal-pane.md) empty-state-no-sessions for display when no sessions exist.

### Wiring

- **scene-hosts-shell**: The `WindowGroup(id: "terminal")` scene MUST host the Terminal Window Shell as its only content.
- **profile-reaches-terminal-view**: The profile resolved through the color-profile ingredient MUST be passed to the terminal-pane terminal view, and a profile change MUST update colors and font without reparenting the view.
- **frame-key-fixed**: The window frame autosave name MUST be the fixed string `"terminal-window"` regardless of how many shells are open.

### Accessibility

- **accessible-window-title**: The window MUST have an accessible window title that distinguishes it from project windows (e.g., "Terminal" or "Terminal — Session Name").

## Layout

```
 WindowGroup(id: "terminal")  [min 600×400, frame "terminal-window"]
┌──────────────┬─────────────────────────────────────────┐
│ Terminal     │ Terminal Pane view                      │
│ Window Shell:│ (colors/font from active Color Profile) │
│ Sessions [+] │                                         │
│  ● Session 1 │  user@host ~ %                          │
│  ○ Session 2 │                                         │
└──────────────┴─────────────────────────────────────────┘
```

The shell supplies the split and session manager; the terminal-pane ingredient fills both halves; the color profile styles the terminal view.

### Composed states

| State | Behavior |
|-------|----------|
| Profile changed | Colors/font applied to terminal view without reparenting |
| Profile deleted while in use | Falls back to Solarized Dark (per color-profile fallback-to-default) |

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Session manager | Terminal Window Shell | Terminal Pane, menu commands | one-way | Window-scoped instance; published as the focused object |
| Active profile ID | Global app storage | Color Profile, every terminal window | one-way | Read from `@AppStorage`; shared across all terminal windows and project windows |
| Window frame | Window | Window Frame Persistence | two-way | Autosave name `"terminal-window"` |
| Focused session manager | Focused window | Menu commands | one-way | `.focusedObject()` dispatch |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| stw-001 | window-group-terminal | Inspect SwiftUI scene declaration | `WindowGroup(id: "terminal")` is registered |
| stw-004 | persist-window-frame | Open terminal window, move to (300, 200), close, reopen | Window restores at (300, 200); autosave name is "terminal-window" |
| stw-005 | min-size-constraints | Attempt to resize window below 600x400 | Window enforces minimum size constraints |
| stw-010 | apply-active-profile, global-profile-storage | Set active profile to Dracula, open terminal window | Terminal renders with Dracula colors (#282a36 background, #f8f8f2 foreground) |
| stw-011 | profile-fallback-default | Set active profile ID in AppStorage to an invalid UUID, open terminal window | Terminal falls back to Solarized Dark (#002b36 background, #839496 foreground) |
| stw-012 | shared-terminal-spec | Compare terminal behavior in standalone window vs. project window terminal pane | Identical PTY lifecycle, OSC handling, session list, and rendering behavior |
| stw-016 | accessible-window-title | Enable VoiceOver, open terminal window | Window title announced as "Terminal" (or similar), distinguishable from project windows |
| stw-017 | scene-hosts-shell, window-group-terminal | Open the terminal window | The scene content is the Terminal Window Shell and nothing else |
| stw-018 | profile-reaches-terminal-view | Change the active profile while a session is running | Terminal colors and font update; the scrollback and view are not reparented |
| stw-019 | frame-key-fixed | Open two standalone windows, move one, close both, reopen | Frame is restored from the single `"terminal-window"` entry |

## Edge Cases

- **Profile deleted while in use**: If the active profile is a custom profile that gets deleted while a standalone terminal window is open, the window MUST fall back to Solarized Dark immediately (per color-profile fallback-to-default). Terminal colors update without reparenting.
- **Standalone window and project window open simultaneously**: Both function independently. Changing the active color profile affects all terminal views across both window types (since profile ID is stored in `@AppStorage`, a global setting).
- **Frame persistence for multiple standalone windows**: All standalone terminal windows share the autosave name `"terminal-window"`. This means only one window's frame is persisted. If multiple standalone windows are needed with independent frame persistence, a future revision MAY introduce per-window identifiers.
- **visionOS window placement**: On visionOS, the system manages window placement. Frame persistence (persist-window-frame) is a no-op on visionOS. Minimum size constraints still apply.

## Platform Notes

- **SwiftUI (macOS)**: Declare the window scene as `WindowGroup(id: "terminal") { StandaloneTerminalView() }`. Set `.frame(minWidth: 600, minHeight: 400)` on the window content. Attach `.background(WindowAccessor(name: "terminal-window", onClose: { sessionManager.terminateAll() }))` for frame persistence and close handling. Read the active profile ID from `@AppStorage("activeProfileId")` and resolve the profile via `TerminalProfile.activeProfile()` with Solarized Dark fallback.
- **SwiftUI (visionOS)**: Same scene structure as macOS. The window opens as a standard visionOS window volume. Frame persistence is not applicable — visionOS manages window placement. Minimum size constraints are respected by the system.
- **Compose**: Declare a `Window` with `rememberWindowState` and a minimum size of 600x400dp. Persist the frame under the fixed key `terminal-window`. Read the active profile from a shared preferences store.
- **React/Web**: Open the terminal view as a route or window with a 600x400px minimum size; persist its frame in `localStorage` under `terminal-window`. Read the active profile ID from `localStorage`.

## Design Decisions

**Decision**: All standalone terminal windows share one frame autosave name, so only one frame is persisted. A future revision MAY introduce per-window identifiers.
**Rationale**: A fixed name keeps restore behavior simple while a per-window identifier scheme is not needed.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [accessibility](agenticdevelopercookbook://guidelines/implementing/accessibility/accessibility) | partial | Accessibility |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |
| [lifecycle-patterns](agenticdevelopercookbook://guidelines/planning/code-quality/lifecycle-patterns) | partial | Best Practices |
| [state-design](agenticdevelopercookbook://guidelines/implementing/ui/state-design) | partial | Best Practices |

> Status is `partial`: this recipe specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-10-04 | Mike Fullerton | Restructured into recipe shape: composes terminal-window-shell, terminal-pane, and color-profile |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |

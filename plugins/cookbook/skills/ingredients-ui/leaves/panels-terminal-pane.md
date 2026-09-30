<!-- leaf: ingredients-ui/panels-terminal-pane · source: ingredients/ui/panels/terminal-pane.md -->

**Rules** (cite as `ingredients-ui/panels-terminal-pane#<slug>`):

- `pty-backed-session` MUST
- `uuid-session-id` MUST
- `observable-properties` MUST
- `default-shell-env` MUST
- `login-shell-launch` MUST
- `term-256color` MUST
- `preserve-env-vars` MUST
- `osc7-directory-update` MUST
- `osc2-title-update` MUST
- `osc7770-custom-commands` MUST
- `poll-foreground-process` MUST
- `update-foreground-name` MUST
- `terminated-on-exit` MUST
- `async-git-branch` MUST
- `stale-branch-discard` MUST
- `non-git-nil-branch` MUST
- `per-window-manager` MUST
- `ordered-session-list` MUST
- `auto-increment-names` MUST
- `optional-working-dir` MUST
- `add-session-select` MUST
- `remove-smart-select` MUST
- `terminate-all-cleanup` MUST
- `nsview-representable` MUST
- `reparent-on-switch` MUST
- `apply-color-profile` MUST
- `palette-color-structure` MUST
- `sidebar-session-list` MUST
- `session-row-display` MUST
- `bind-selected-session` MUST
- `add-session-button` MUST
- `row-context-menu` MUST
- `empty-state-no-sessions` MUST
- `project-shell-settings` MUST

# Terminal Pane

## Overview

A multi-session terminal pane that provides PTY-backed shell sessions within the workspace. Bundles five cooperating parts: terminal sessions (PTY lifecycle and state), a session manager (per-window session orchestration), a terminal view (SwiftTerm rendering with reparenting), a session list sidebar (selection and metadata display), and terminal profiles (shell and project-level settings). Derived from scratching-post terminal subsystem.

## Terminology

| Term | Definition |
|------|-----------|
| PTY | Pseudo-terminal — a kernel-level pair of file descriptors that connect a terminal emulator to a shell process |
| Terminal session | A single PTY-backed shell instance with its own state, scrollback, and metadata |
| Session manager | Per-window controller that owns an ordered list of sessions and manages their lifecycle |
| Terminal view | The visual rendering surface for a terminal session, backed by SwiftTerm on Apple platforms |
| Reparenting | Moving a terminal's NSView from one container to another without destroying scrollback or state |
| OSC | Operating System Command — an escape sequence used for terminal-to-app communication |
| Foreground process | The currently running process in the terminal's PTY, detected via `tcgetpgrp` |
| Dot color | A user-assignable colored indicator displayed in the session list row |
| Custom subtitle | Key-value metadata injected via OSC 7770 and displayed beneath the session name |

## Behavioral Requirements

### Terminal session

- **pty-backed-session**: Each terminal session MUST be backed by a PTY using a terminal emulator library (SwiftTerm on Apple platforms).
- **uuid-session-id**: Each session MUST have a unique UUID-based identifier.
- **observable-properties**: Each session MUST publish the following observable properties:
  - `name` — user-visible session name (editable)
  - `terminalTitle` — title set by the shell via OSC 2
  - `currentWorkingDirectory` — path set via OSC 7
  - `gitBranch` — current git branch for the working directory
  - `foregroundProcess` — name of the currently running foreground process
  - `dotColors` — array of user-assignable colored indicators
  - `customSubtitles` — dictionary of key-value subtitle metadata
  - `state` — enum: `.running` or `.terminated`
- **default-shell-env**: The session MUST read the user's default shell from the `$SHELL` environment variable. If `$SHELL` is unset or empty, it MUST fall back to `/bin/zsh`.
- **login-shell-launch**: The shell MUST be launched as a login shell by prefixing the process name with `"-"` (e.g., `"-zsh"`).
- **term-256color**: The session MUST set `TERM=xterm-256color` in the child process environment.
- **preserve-env-vars**: The session MUST preserve the following environment variables from the parent process: `HOME`, `USER`, `LOGNAME`, `PATH`, `LANG`, `LC_ALL`, `LC_CTYPE`.

### OSC escape handling

- **osc7-directory-update**: The session MUST handle OSC 7 (directory update). On receipt, it MUST update `currentWorkingDirectory` by parsing the `file://` URL and MUST trigger an asynchronous git branch detection for the new directory.
- **osc2-title-update**: The session MUST handle OSC 2 (title update). On receipt, it MUST update `terminalTitle`.
- **osc7770-custom-commands**: The session MUST handle custom OSC 7770 with the following sub-commands:
  - `color=#rrggbb` — sets a dot color on the session
  - `subtitle:key=value` — sets or updates a custom subtitle entry
  - `clear-subtitle:key` — removes a specific custom subtitle entry
  - `clear-all-subtitles` — removes all custom subtitle entries

### Process monitoring

- **poll-foreground-process**: The session MUST poll the foreground process every 1.5 seconds using `tcgetpgrp` to get the foreground process group ID, then `proc_pidpath` to resolve the process name.
- **update-foreground-name**: When the foreground process changes, the session MUST update the `foregroundProcess` property.
- **terminated-on-exit**: When the shell process exits, the session MUST transition `state` to `.terminated`.

### Git branch detection

- **async-git-branch**: Git branch detection MUST be performed asynchronously with a 2-second timeout by running `git rev-parse --abbrev-ref HEAD` in the session's current working directory.
- **stale-branch-discard**: Git branch detection MUST use a stale-request-tracking mechanism (UUID per request) so that results from outdated directory changes are discarded.
- **non-git-nil-branch**: If the directory is not a git repository, `gitBranch` MUST be set to `nil`.

### Session manager

- **per-window-manager**: Each window MUST have its own session manager instance. Session managers MUST NOT be shared across windows.
- **ordered-session-list**: The session manager MUST maintain an ordered list of sessions and a selected session ID.
- **auto-increment-names**: Session names MUST be auto-incremented using the pattern "Session 1", "Session 2", etc. The counter MUST be monotonically increasing (not reused after deletion).
- **optional-working-dir**: The session manager MAY accept an optional working directory (for project context). When provided, new sessions MUST start in that directory.
- **add-session-select**: `addSession()` MUST create a new session, append it to the list, select it, and return it.
- **remove-smart-select**: `removeSession(id:)` MUST terminate the session's PTY, remove it from the list, and apply smart selection: prefer the previous session in the list, then the next session, then nil if none remain.
- **terminate-all-cleanup**: `terminateAll()` MUST terminate all sessions' PTYs and clear the list. This MUST be called on window close.

### Terminal view

- **nsview-representable**: The terminal view MUST be implemented as an `NSViewRepresentable` (macOS) or `UIViewRepresentable` (iOS/visionOS) wrapper containing a container `NSView`/`UIView`.
- **reparent-on-switch**: On session change, the terminal view MUST reparent the selected session's terminal view into the container — not destroy and recreate it. This preserves scrollback history and cursor state.
- **apply-color-profile**: On profile change, the terminal view MUST apply the new color profile (foreground, background, cursor, selection, 16 ANSI colors, font, cursor style) without reparenting the view.
- **palette-color-structure**: Profile colors MUST be applied using the color-profile component's palette structure: FG, BG, cursor, selection, and exactly 16 ANSI colors (indices 0-15).

### Session list sidebar

- **sidebar-session-list**: The session list MUST be displayed as a sidebar list showing one row per session.
- **session-row-display**: Each session row MUST display:
  - Dot color indicator(s) (if any assigned)
  - Session name (primary text)
  - Subtitle lines using the metadata-line component for: working directory (folder icon, middle-truncated path), git branch (branch icon), and foreground process (terminal icon)
- **bind-selected-session**: The session list MUST bind to the session manager's selected session ID for selection state.
- **add-session-button**: The session list MUST include an add button (`+`) that creates a new session via the session manager.
- **row-context-menu**: Each session row MUST have a context menu with at least: "Rename" and "Close" actions.

### Empty state

- **empty-state-no-sessions**: When no sessions exist, the terminal pane MUST display an empty state (per `ui/empty-state.md`) with:
  - Icon: `terminal` (SF Symbol) or platform equivalent
  - Heading: "No active terminal session"
  - Description: "Click + to open a new terminal session"
  - Optional action button: "New Session" (calls `addSession()`)

### Project settings

- **project-shell-settings**: The following settings MUST be available per-project in the settings window:
  - `defaultShell` — a string picker with options: `/bin/zsh`, `/bin/bash`, `/bin/sh`, `/usr/local/bin/fish`, `/opt/homebrew/bin/fish`. Overrides `$SHELL` when set.
  - `autoOpenTerminal` — a boolean that, when enabled, automatically opens a terminal session when the project is opened.

## Appearance

### Terminal pane layout

```
┌───────────────┬────────────────────────────────────┐
│ Sessions  [+] │                                    │
├───────────────┤                                    │
│               │                                    │
│ ● Session 1   │  user@host ~ %                     │
│   ~/projects  │  ls -la                            │
│   main        │  total 42                          │
│   zsh         │  drwxr-xr-x  5 user staff  160 ...│
│               │  -rw-r--r--  1 user staff  230 ...│
│ ○ Session 2   │                                    │
│   ~/docs      │                                    │
│   bash        │                                    │
│               │                                    │
│               │                                    │
│               │                                    │
└───────────────┴────────────────────────────────────┘
```

### Session row detail

```
┌───────────────────┐
│ ● Session 1       │  ← dot color + name
│  📁 ~/projects    │  ← metadata-line: working directory (middle-truncated)
│  🌿 main          │  ← metadata-line: git branch
│  ⬛ zsh           │  ← metadata-line: foreground process
└───────────────────┘
```

### Empty state

```
┌────────────────────────────────────────────────────┐
│                                                    │
│                                                    │
│                   ⬛                               │
│         No active terminal session                 │
│     Click + to open a new terminal session         │
│              [New Session]                         │
│                                                    │
│                                                    │
└────────────────────────────────────────────────────┘
```

- **Sidebar width**: 180–220pt, resizable
- **Session row spacing**: 4pt between dot/name line and metadata lines
- **Metadata lines**: Use metadata-line component (12pt secondary icon + caption text)
- **Dot color**: 8pt filled circle, leading the session name
- **Terminal background**: Determined by active color profile
- **Terminal font**: Determined by active color profile (monospaced)


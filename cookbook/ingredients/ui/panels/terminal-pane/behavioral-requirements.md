
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


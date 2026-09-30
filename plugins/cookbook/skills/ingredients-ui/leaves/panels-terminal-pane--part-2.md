<!-- leaf: ingredients-ui/panels-terminal-pane--part-2 · source: ingredients/ui/panels/terminal-pane.md -->

# Terminal Pane — continued (part 2)

**Rules** (cite as `ingredients-ui/panels-terminal-pane--part-2#<slug>`):

- `keyboard-nav-sessions` MUST
- `add-button-label` MUST
- `row-announce-details` MUST
- `keyboard-context-menu` MUST
- `voiceover-terminal-nav` MUST
- `empty-state-accessible` MUST
- `terminated-announce` MUST

## Accessibility

- **keyboard-nav-sessions**: The session list MUST be keyboard-navigable. Arrow keys MUST move selection between sessions.
- **add-button-label**: The add button MUST have an accessible label: "New Terminal Session".
- **row-announce-details**: Each session row MUST announce: session name, working directory, git branch (if present), and foreground process via a combined accessibility label.
- **keyboard-context-menu**: The context menu MUST be accessible via keyboard (e.g., Shift+F10 or Control+Click equivalent).
- **voiceover-terminal-nav**: The terminal view MUST support VoiceOver cursor navigation for reading terminal output.
- **empty-state-accessible**: The empty state MUST follow empty-state accessibility requirements (heading announced first, icon decorative).
- **terminated-announce**: The `.terminated` state MUST be announced to screen readers when a session's shell exits.

## Configuration

This ingredient has no configurable options.

## Platform Notes

- **SwiftUI (macOS)**: Use `NSViewRepresentable` wrapping a container `NSView`. SwiftTerm provides `TerminalView` (an `NSView` subclass) — do not recreate it per session switch; instead, remove it from the old container and add it to the new container via `addSubview` / `removeFromSuperview`. Apply color profiles via SwiftTerm's `installColors(foreground:background:cursor:selection:ansi:)` and `font` property. PTY creation: use `forkpty()` or `posix_openpt()` + `grantpt()` + `unlockpt()`. Process monitoring: `tcgetpgrp(fd)` for PGID, `proc_pidpath(pid, buf, bufSize)` for process path. Session list: `List(selection:)` with `ForEach` over session manager's sessions. Context menu via `.contextMenu`. The `+` button in the sidebar header via a `toolbar` item scoped to the sidebar.
- **SwiftUI (iOS / visionOS)**: Use `UIViewRepresentable` wrapping a container `UIView`. SwiftTerm provides `TerminalView` as a `UIView` subclass. Reparenting approach is identical. On iOS, the session list may be presented as a sheet or popover rather than a persistent sidebar, depending on size class. On visionOS, use a `NavigationSplitView` with the session list in the sidebar column. PTY APIs (`forkpty`, `tcgetpgrp`) are available on iOS but sandboxing restrictions may limit shell execution to developer/enterprise contexts.
- **General**: The terminal emulator library (SwiftTerm) handles VT100/xterm escape sequence parsing, scrollback buffer management, and text rendering. The session layer is responsible for PTY lifecycle, environment setup, OSC dispatch, and process monitoring. The view layer is responsible for reparenting and profile application.

## Privacy

- **Data collected**: Terminal output is rendered in-memory by SwiftTerm. Custom subtitles and dot colors are session-ephemeral.
- **Storage**: No terminal content is persisted to disk. Project settings (defaultShell, autoOpenTerminal) are stored in the project's settings file.
- **Transmission**: None — terminal content never leaves the device.
- **Retention**: Session data exists only for the lifetime of the session. Settings persist until changed.

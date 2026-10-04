
- **Shell not found**: If the configured shell path does not exist (e.g., fish not installed), the session MUST fall back to `/bin/zsh` and log a warning. It MUST NOT crash.
- **PTY allocation failure**: If PTY allocation fails, the session MUST display an error message in the terminal view area and log an error. It MUST NOT crash.
- **Rapid session switching**: Reparenting MUST complete without flicker. If a session switch occurs while a reparenting is in progress, the latest switch MUST win.
- **Very long session name**: Session name SHOULD truncate with trailing ellipsis in the sidebar row.
- **Many sessions (50+)**: The session list MUST remain scrollable and performant. Consider virtualized/recycled list.
- **Git branch detection timeout**: If `git rev-parse` exceeds 2 seconds, the request MUST be cancelled and `gitBranch` left unchanged. No error shown to user.
- **Git not installed**: If `git` is not available on PATH, git branch detection MUST silently set `gitBranch` to nil. No error shown.
- **OSC 7770 malformed payload**: Invalid sub-commands or malformed hex colors MUST be silently ignored. Log at debug level.
- **Process monitoring after shell exit**: Polling MUST stop when the session transitions to `.terminated`. Timer MUST be invalidated.
- **Large scrollback buffer**: SwiftTerm should handle large scrollback (10,000+ lines) without excessive memory growth. Rely on library defaults.
- **Session terminated while selected**: The terminated session SHOULD remain visible (showing final output) until the user removes it or switches away.
- **Multiple dot colors**: A session MAY have multiple dot colors (from multiple OSC 7770 color commands). Display them in order.
- **Window restored after crash**: Session manager MUST NOT attempt to restore PTY sessions from a previous run. Sessions are ephemeral.
- **Environment variable conflicts**: If `defaultShell` project setting and `$SHELL` both exist, `defaultShell` MUST take precedence.
- **Non-UTF-8 output**: The terminal emulator library (SwiftTerm) handles encoding. Invalid sequences SHOULD be rendered as replacement characters, not cause a crash.


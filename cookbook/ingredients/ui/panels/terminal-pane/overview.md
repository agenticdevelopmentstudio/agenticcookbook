
A multi-session terminal pane that provides PTY-backed shell sessions within the workspace. Bundles five cooperating parts: terminal sessions (PTY lifecycle and state), a session manager (per-window session orchestration), a terminal view (SwiftTerm rendering with reparenting), a session list sidebar (selection and metadata display), and terminal profiles (shell and project-level settings). Derived from scratching-post terminal subsystem.

### Terminology

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

